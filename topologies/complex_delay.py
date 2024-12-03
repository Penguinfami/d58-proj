
import json
import sched
import time
import random
import threading
import signal
import sys

scheduler = sched.scheduler(time.time, time.sleep)


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
    s13 = net.addSwitch('s13', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s16 = net.addSwitch('s16', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s17 = net.addSwitch('s17', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s15 = net.addSwitch('s15', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s10 = net.addSwitch('s10', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s9 = net.addSwitch('s9', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s11 = net.addSwitch('s11', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s14 = net.addSwitch('s14', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s12 = net.addSwitch('s12', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, protocols="OpenFlow10")
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch, protocols="OpenFlow10")

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)

    info( '*** Add links\n')
    s3s2 = {'delay':'3ms'}
    net.addLink(s3, s2, cls=TCLink , **s3s2)
    s2s5 = {'delay':'6ms'}
    net.addLink(s2, s5, cls=TCLink , **s2s5)
    s2s1 = {'delay':'1ms'}
    net.addLink(s2, s1, cls=TCLink , **s2s1)
    s2s4 = {'delay':'1ms'}
    net.addLink(s2, s4, cls=TCLink , **s2s4)
    s1s4 = {'delay':'2ms'}
    net.addLink(s1, s4, cls=TCLink , **s1s4)
    s3s16 = {'delay':'5ms'}
    net.addLink(s3, s16, cls=TCLink , **s3s16)
    s16s2 = {'delay':'2ms'}
    net.addLink(s16, s2, cls=TCLink , **s16s2)
    s16s1 = {'delay':'4ms'}
    net.addLink(s16, s1, cls=TCLink , **s16s1)
    s5s4 = {'delay':'4ms'}
    net.addLink(s5, s4, cls=TCLink , **s5s4)
    s4s8 = {'delay':'6ms'}
    net.addLink(s4, s8, cls=TCLink , **s4s8)
    s5s8 = {'delay':'4ms'}
    net.addLink(s5, s8, cls=TCLink , **s5s8)
    s3s5 = {'delay':'4ms'}
    net.addLink(s3, s5, cls=TCLink , **s3s5)
    s3s6 = {'delay':'2ms'}
    net.addLink(s3, s6, cls=TCLink , **s3s6)
    s6s7 = {'delay':'6ms'}
    net.addLink(s6, s7, cls=TCLink , **s6s7)
    s6s10 = {'delay':'2ms'}
    net.addLink(s6, s10, cls=TCLink , **s6s10)
    s10s7 = {'delay':'3ms'}
    net.addLink(s10, s7, cls=TCLink , **s10s7)
    s7s5 = {'delay':'1ms'}
    net.addLink(s7, s5, cls=TCLink , **s7s5)
    s7s9 = {'delay':'1ms'}
    net.addLink(s7, s9, cls=TCLink , **s7s9)
    s5s9 = {'delay':'2ms'}
    net.addLink(s5, s9, cls=TCLink , **s5s9)
    s8s11 = {'delay':'1ms'}
    net.addLink(s8, s11, cls=TCLink , **s8s11)
    s12s8 = {'delay':'3ms'}
    net.addLink(s12, s8, cls=TCLink , **s12s8)
    s9s12 = {'delay':'2ms'}
    net.addLink(s9, s12, cls=TCLink , **s9s12)
    s9s14 = {'delay':'2ms'}
    net.addLink(s9, s14, cls=TCLink , **s9s14)
    s14s12 = {'delay':'6ms'}
    net.addLink(s14, s12, cls=TCLink , **s14s12)
    s12s11 = {'delay':'2ms'}
    net.addLink(s12, s11, cls=TCLink , **s12s11)
    s12s15 = {'delay':'3ms'}
    net.addLink(s12, s15, cls=TCLink , **s12s15)
    s11s15 = {'delay':'2ms'}
    net.addLink(s11, s15, cls=TCLink , **s11s15)
    s14s15 = {'delay':'2ms'}
    net.addLink(s14, s15, cls=TCLink , **s14s15)
    s10s13 = {'delay':'2ms'}
    net.addLink(s10, s13, cls=TCLink , **s10s13)
    s10s14 = {'delay':'9ms'}
    net.addLink(s10, s14, cls=TCLink , **s10s14)
    s14s17 = {'delay':'9ms'}
    net.addLink(s14, s17, cls=TCLink , **s14s17)
    s13s17 = {'delay':'2ms'}
    net.addLink(s13, s17, cls=TCLink , **s13s17)
    s17s15 = {'delay':'4ms'}
    net.addLink(s17, s15, cls=TCLink , **s17s15)
    s16h1 = {'delay':'0ms'}
    net.addLink(s16, h1, cls=TCLink , **s16h1)
    h2s17 = {'delay':'0ms'}
    net.addLink(h2, s17, cls=TCLink , **h2s17)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s13').start([c0])
    net.get('s5').start([c0])
    net.get('s8').start([c0])
    net.get('s16').start([c0])
    net.get('s17').start([c0])
    net.get('s4').start([c0])
    net.get('s15').start([c0])
    net.get('s1').start([c0])
    net.get('s10').start([c0])
    net.get('s9').start([c0])
    net.get('s11').start([c0])
    net.get('s7').start([c0])
    net.get('s14').start([c0])
    net.get('s3').start([c0])
    net.get('s12').start([c0])
    net.get('s2').start([c0])
    net.get('s6').start([c0])

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

    storeTopologyState(net, "networkdata.json", "w")

    start_http_server(h1, 1)
    start_http_server(h2, 2)

    setup_link_state_changes(net)

    setupScheduleTopologyStoring(net)
    
    scheduler_thread = threading.Thread(target=schedule_events)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    signal.signal(signal.SIGINT, handle_ctrl_c)
    CLI(net)
    return net

updatedParams = {}

def handle_ctrl_c(signal, frame):
    print("Ctrl-C pressed. Stopping Mininet...")
    sys.exit(0)

def start_http_server(host, serverNumber):
    "Start an HTTP server on a specific host."
    print("Starting HTTP server")
    command = 'cd ./server%d; python server.py --bind %s 80 > %s_http.log 2>&1 &' % (serverNumber, host.IP(), host.name)
    print(command)
    # Run the server in the background
    host.cmd(command)

def schedule_events():
    scheduler.run()

def setup_link_state_changes(net):
    for link in net.links:
        scheduler.enter(5, 1, scheduleLinkStateUpdates, [link])

def scheduleLinkStateUpdates(link):
    #print("New link delay update" + link.intf1.name + " t=" + str(time.time()))
    randomDelay = random.randint(1, 10)
    randomLoss = random.randint(0, 10)
    randomBandwidth = random.randint(1, 100)/10.0
    attribute = sys.argv[1]
    if attribute == "delay":
        link.intf1.config(delay=(str(randomDelay) + 'ms'))
        if link.intf1.name not in updatedParams:
            updatedParams[link.intf1.name] = link.intf1.params
        updatedParams[link.intf1.name]["delay"] = str(randomDelay) + 'ms'
    elif attribute == "bw":
        #print("Updating bw to %f" % randomBandwidth)
        link.intf1.config(bw=randomBandwidth)
        if link.intf1.name not in updatedParams:
            updatedParams[link.intf1.name] = link.intf1.params
        updatedParams[link.intf1.name]["bw"] = str(randomBandwidth)
    elif attribute == "loss":
        link.intf1.config(loss=randomBandwidth)
        if link.intf1.name not in updatedParams:
            updatedParams[link.intf1.name] = link.intf1.params
        updatedParams[link.intf1.name]["loss"] = str(randomBandwidth)
    elif attribute == "delaybw":
        link.intf1.config(delay=(str(randomDelay) + 'ms'))
        if link.intf1.name not in updatedParams:
            updatedParams[link.intf1.name] = link.intf1.params
        updatedParams[link.intf1.name]["delay"] = str(randomDelay) + 'ms'
        link.intf1.config(bw=randomBandwidth)
        updatedParams[link.intf1.name]["bw"] = str(randomBandwidth)
    else:
        if link.intf1.name not in updatedParams:
            updatedParams[link.intf1.name] = link.intf1.params   
    randomTime = random.randint(8, 45)
    scheduler.enter(randomTime, 1, scheduleLinkStateUpdates, [link])


def scheduleTopologyStoring(net, filename):
    #print(updatedParams)
    storeTopologyState(net, filename, "w")
    scheduler.enter(5, 1, scheduleTopologyStoring, [net, "networkdata.json"])


def setupScheduleTopologyStoring(net):
    scheduler.enter(5, 1, scheduleTopologyStoring, [net, "networkdata.json"])

def storeTopologyState(net, filename, action):
    hostToIp = {}
    for host in net.hosts:
        hostToIp[host.name] = host.IP()
    macToItf = {}
    for switch in net.switches:
        for intf in switch.intfs.values():
            #print(intf, intf.name, switch.name, intf.MAC())
            macToItf[intf.MAC()] = intf.name
    
    toWrite = {
        "links": [],
        "interfaces": {}
    }

    for link in net.links:
        #print( link.intf1.params, link.intf1.node.name, link.intf1, link.intf1.MAC(), link.intf1.IP(), link.intf2, link.intf2.node.name, link.intf2.MAC(), link.intf2.IP(), link.intf1.params)
        #print(link.intf1.config())
        startName = link.intf1.node.name
        startIP = None if startName not in hostToIp else hostToIp[startName]
        endName = link.intf2.node.name 
        endIP = None if endName not in hostToIp else hostToIp[endName]
        startMAC = link.intf1.MAC()
        endMAC = link.intf2.MAC()
        if link.intf1.name in updatedParams:
            startParams = updatedParams[link.intf1.name]
        else:
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
    with open(filename, action) as f:
        json.dump(toWrite, f)

    
if __name__ == '__main__':
    setLogLevel( 'info' )
    net = myNetwork()
    net.build()


