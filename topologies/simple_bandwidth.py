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

    c1=net.addController(name='c1',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6634)

    info( '*** Add switches\n')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)

    info( '*** Add links\n')
    s1h1 = {'bw':1}
    net.addLink(s1, h1, cls=TCLink , **s1h1)
    h1s2 = {'bw':1}
    net.addLink(h1, s2, cls=TCLink , **h1s2)
    s2h2 = {'bw':1}
    net.addLink(s2, h2, cls=TCLink , **s2h2)
    h2s3 = {'bw':1}
    net.addLink(h2, s3, cls=TCLink , **h2s3)
    s3s1 = {'bw':1}
    net.addLink(s3, s1, cls=TCLink , **s3s1)
    h2s6 = {'bw':2}
    net.addLink(h2, s6, cls=TCLink , **h2s6)
    s6s7 = {'bw':2}
    net.addLink(s6, s7, cls=TCLink , **s6s7)
    s7h3 = {'bw':2}
    net.addLink(s7, h3, cls=TCLink , **s7h3)
    h3s8 = {'bw':1}
    net.addLink(h3, s8, cls=TCLink , **h3s8)
    s8h2 = {'bw':1}
    net.addLink(s8, h2, cls=TCLink , **s8h2)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s2').start([c0])
    net.get('s7').start([c1])
    net.get('s1').start([c0])
    net.get('s8').start([c1])
    net.get('s3').start([c0])
    net.get('s6').start([c1])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

