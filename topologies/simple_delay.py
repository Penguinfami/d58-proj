import json
#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, protocols="OpenFlow10")

    info( '*** Add hosts\n')
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)

    info( '*** Add links\n')
    s1h1 = {'delay':'1ms'}
    net.addLink(s1, h1, cls=TCLink , **s1h1)
    h1s2 = {'delay':'1ms'}
    net.addLink(h1, s2, cls=TCLink , **h1s2)
    s2h2 = {'delay':'1ms'}
    net.addLink(s2, h2, cls=TCLink , **s2h2)
    h2s3 = {'delay':'1ms'}
    net.addLink(h2, s3, cls=TCLink , **h2s3)
    s3s1 = {'delay':'1ms'}
    net.addLink(s3, s1, cls=TCLink , **s3s1)
    h2s6 = {'delay':'1ms'}
    net.addLink(h2, s6, cls=TCLink , **h2s6)
    s6s7 = {'delay':'1ms'}
    net.addLink(s6, s7, cls=TCLink , **s6s7)
    s7h3 = {'delay':'1ms'}
    net.addLink(s7, h3, cls=TCLink , **s7h3)
    h3s8 = {'delay':'2ms'}
    net.addLink(h3, s8, cls=TCLink , **h3s8)
    s8h2 = {'delay':'2ms'}
    net.addLink(s8, h2, cls=TCLink , **s8h2)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s6').start([c0])
    net.get('s2').start([c0])
    net.get('s8').start([c0])
    net.get('s7').start([c0])
    net.get('s3').start([c0])
    net.get('s1').start([c0])

    info( '*** Post configure switches and hosts\n')

    s1.cmd('ifconfig s1-eth1 10.0.0.11')
    s1.cmd('ifconfig s1-eth2 10.0.0.21')
    s7.cmd('ifconfig s7-eth1 10.0.0.18')
    s7.cmd('ifconfig s7-eth2 10.0.0.28')
    s6.cmd('ifconfig s6-eth1 10.0.0.16')
    s6.cmd('ifconfig s6-eth2 10.0.0.26')
    s3.cmd('ifconfig s3-eth1 10.0.0.13')
    s3.cmd('ifconfig s3-eth2 10.0.0.23')
    s8.cmd('ifconfig s8-eth1 10.0.0.18')
    s8.cmd('ifconfig s8-eth2 10.0.0.28')
    s2.cmd('ifconfig s2-eth1 10.0.0.12')
    s2.cmd('ifconfig s2-eth2 10.0.0.22')

    hostToIp = {}
    for host in net.hosts:
        hostToIp[host.name] = host.IP()
    macToItf = {}
    for switch in net.switches:
        for port in switch.ports:
            print(port)
            print(switch.ports[port])
            print(port.name,port.MAC())  # MAC address of each port
        for intf in switch.intfs.values():
            print(intf, intf.name, switch.name, intf.MAC())
            macToItf[intf.MAC()] = intf.name
    
    toWrite = {
        "links": [],
        "interfaces": {}
    }

    print("Switch port MAC addresses:")

    for link in net.links:
        print( link.intf1.params, link.intf1.node.name, link.intf1, link.intf1.MAC(), link.intf1.IP(), link.intf2, link.intf2.node.name, link.intf2.MAC(), link.intf2.IP(), link.intf2.params)
        startName = link.intf1.node.name
        startIP = None if startName not in hostToIp else hostToIp[startName]
        endName = link.intf2.node.name 
        endIP = None if endName not in hostToIp else hostToIp[endName]
        startMAC = link.intf1.MAC()
        endMAC = link.intf2.MAC()
        startParams = link.intf1.params
        startPort = link.intf1.node.ports.get(link.intf1)  # Port number for intf1
        endPort = link.intf2.node.ports.get(link.intf2)  # Port number for intf2

        toWrite["links"].append({
            "startName": startName,
            "startInterface": link.intf1.name,
            "startIP": startIP,
            "startMAC": startMAC,
            "endInterface": link.intf2.name,
            "endName": endName,
            "endIP": endIP,
            "endMAC": endMAC,
            "params": startParams,
            "startPort": startPort,
            "endPort": endPort
        })
        toWrite["interfaces"][link.intf1.name] = {
            "node": startName,
            "mac": startMAC
        }

        toWrite["interfaces"][link.intf2.name] = {
            "node": endName,
            "mac": endMAC
        }
    json_string = json.dumps(toWrite)
    with open("networkdata.json", "w") as f:
        json.dump(toWrite, f)

    start_http_server(h1, 1)
    start_http_server(h2, 2)

    CLI(net)
    return net

def start_http_server(host, serverNumber):
    "Start an HTTP server on a specific host."
    print("Starting HTTP server")
    command = 'cd ./server%d; python server.py --bind %s 80 > %s_http.log 2>&1 &' % (serverNumber, host.IP(), host.name)
    print(command)
    # Run the server in the background
    host.cmd(command)

if __name__ == '__main__':
    setLogLevel( 'info' )
    net = myNetwork()
    net.build()


