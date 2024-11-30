#!/usr/bin/env python
import json

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
                   ipBase='10.0.0.0/8',
                   switch=OVSKernelSwitch)

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s13 = net.addSwitch('s13', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch,protocols="OpenFlow10")
    s11 = net.addSwitch('s11', cls=OVSKernelSwitch,protocols="OpenFlow10")
    s16 = net.addSwitch('s16', cls=OVSKernelSwitch,protocols="OpenFlow10")
    s9 = net.addSwitch('s9', cls=OVSKernelSwitch,protocols="OpenFlow10")
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s12 = net.addSwitch('s12', cls=OVSKernelSwitch,protocols="OpenFlow10")
    s14 = net.addSwitch('s14', cls=OVSKernelSwitch,protocols="OpenFlow10")
    s10 = net.addSwitch('s10', cls=OVSKernelSwitch,protocols="OpenFlow10")
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch,protocols="OpenFlow10")
    s15 = net.addSwitch('s15', cls=OVSKernelSwitch,protocols="OpenFlow10")
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, protocols="OpenFlow10")

    info( '*** Add hosts\n')
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.23', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.21', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.22', defaultRoute=None)

    info( '*** Add links\n')
    h1s1 = {'delay':'1'}
    net.addLink(h1, s1, cls=TCLink , **h1s1)
    s1s2 = {'delay':'1'}
    net.addLink(s1, s2, cls=TCLink , **s1s2)
    s2s3 = {'delay':'1'}
    net.addLink(s2, s3, cls=TCLink , **s2s3)
    s3s4 = {'delay':'1'}
    net.addLink(s3, s4, cls=TCLink , **s3s4)
    s4s5 = {'delay':'1'}
    net.addLink(s4, s5, cls=TCLink , **s4s5)
    s5s6 = {'delay':'1'}
    net.addLink(s5, s6, cls=TCLink , **s5s6)
    s6s7 = {'delay':'1'}
    net.addLink(s6, s7, cls=TCLink , **s6s7)
    s7s8 = {'delay':'1'}
    net.addLink(s7, s8, cls=TCLink , **s7s8)
    s8s9 = {'delay':'1'}
    net.addLink(s8, s9, cls=TCLink , **s8s9)
    s9s10 = {'delay':'1'}
    net.addLink(s9, s10, cls=TCLink , **s9s10)
    s10s11 = {'delay':'1'}
    net.addLink(s10, s11, cls=TCLink , **s10s11)
    s11s12 = {'delay':'1'}
    net.addLink(s11, s12, cls=TCLink , **s11s12)
    s12s13 = {'delay':'1'}
    net.addLink(s12, s13, cls=TCLink , **s12s13)
    s13s14 = {'delay':'1'}
    net.addLink(s13, s14, cls=TCLink , **s13s14)
    s14s15 = {'delay':'1'}
    net.addLink(s14, s15, cls=TCLink , **s14s15)
    s15s16 = {'delay':'1'}
    net.addLink(s15, s16, cls=TCLink , **s15s16)
    s16h2 = {'delay':'1'}
    net.addLink(s16, h2, cls=TCLink , **s16h2)
    s8h3 = {'delay':'1'}
    net.addLink(s8, h3, cls=TCLink , **s8h3)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s13').start([c0])
    net.get('s1').start([c0])
    net.get('s7').start([c0])
    net.get('s11').start([c0])
    net.get('s16').start([c0])
    net.get('s9').start([c0])
    net.get('s5').start([c0])
    net.get('s12').start([c0])
    net.get('s14').start([c0])
    net.get('s10').start([c0])
    net.get('s4').start([c0])
    net.get('s15').start([c0])
    net.get('s6').start([c0])
    net.get('s3').start([c0])
    net.get('s8').start([c0])
    net.get('s2').start([c0])


    info( '*** Post configure switches and hosts\n')
    s5.cmd('ifconfig s5-eth1 10.0.0.5')
    s13.cmd('ifconfig s13-eth1 10.0.0.13')
    s4.cmd('ifconfig s4-eth1 10.0.0.4')
    s1.cmd('ifconfig s1-eth1 10.0.0.1')
    s16.cmd('ifconfig s16-eth1 10.0.0.16')
    s12.cmd('ifconfig s12-eth1 10.0.0.12')
    s7.cmd('ifconfig s7-eth1 10.0.0.8')
    s6.cmd('ifconfig s6-eth1 10.0.0.6')
    s9.cmd('ifconfig s9-eth1 10.0.0.9')
    s14.cmd('ifconfig s14-eth1 10.0.0.14')
    s10.cmd('ifconfig s10-eth1 10.0.0.10')
    s3.cmd('ifconfig s3-eth1 10.0.0.3')
    s11.cmd('ifconfig s11-eth1 10.0.0.11')
    s15.cmd('ifconfig s15-eth1 10.0.0.15')
    s8.cmd('ifconfig s8-eth1 10.0.0.8')
    s2.cmd('ifconfig s2-eth1 10.0.0.2')

    info( '*** Post configure switches and hosts\n')
    
    print(dir(net))
    print("IP to MAC mappings:")
    hostToIp = {}
    for host in net.hosts:
        print("Host %s: IP = %s, MAC = %s" % (host.name, host.IP(), host.MAC()))
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
        print( link.intf1.params, link.intf1.node.name, link.intf1, link.intf1.MAC(), link.intf1.IP(), link.intf2.node.name, link.intf2.MAC(), link.intf2.params)
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
    print(json_string)
    with open("networkdata.json", "w") as f:
        json.dump(toWrite, f)
    print(dir(net.links[0]))

    CLI(net)
    return net

if __name__ == '__main__':
    setLogLevel( 'info' )
    net = myNetwork()
    net.build()

