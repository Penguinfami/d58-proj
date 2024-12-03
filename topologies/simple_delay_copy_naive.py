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
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s10 = net.addSwitch('s10', cls=OVSKernelSwitch)
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
    s11 = net.addSwitch('s11', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)

    info( '*** Add links\n')
    s3s1 = {'delay':'1'}
    net.addLink(s3, s1, cls=TCLink , **s3s1)
    s6s7 = {'delay':'1'}
    net.addLink(s6, s7, cls=TCLink , **s6s7)
    s3s4 = {'delay':'1'}
    net.addLink(s3, s4, cls=TCLink , **s3s4)
    s2s4 = {'delay':'1'}
    net.addLink(s2, s4, cls=TCLink , **s2s4)
    s4h2 = {'delay':'1'}
    net.addLink(s4, h2, cls=TCLink , **s4h2)
    s5s6 = {'delay':'1'}
    net.addLink(s5, s6, cls=TCLink , **s5s6)
    s5s8 = {'delay':'2'}
    net.addLink(s5, s8, cls=TCLink , **s5s8)
    s1s10 = {'delay':'1'}
    net.addLink(s1, s10, cls=TCLink , **s1s10)
    s10s2 = {'delay':'1'}
    net.addLink(s10, s2, cls=TCLink , **s10s2)
    s10h1 = {'delay':'0'}
    net.addLink(s10, h1, cls=TCLink , **s10h1)
    s7s11 = {'delay':'1'}
    net.addLink(s7, s11, cls=TCLink , **s7s11)
    s8s11 = {'delay':'2'}
    net.addLink(s8, s11, cls=TCLink , **s8s11)
    s11h4 = {'delay':'0'}
    net.addLink(s11, h4, cls=TCLink , **s11h4)
    h3s5 = {'delay':'1'}
    net.addLink(h3, s5, cls=TCLink , **h3s5)
    s4s5 = {'delay':'1'}
    net.addLink(s4, s5, cls=TCLink , **s4s5)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s7').start([c0])
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])
    net.get('s10').start([c0])
    net.get('s8').start([c0])
    net.get('s5').start([c0])
    net.get('s6').start([c0])
    net.get('s11').start([c0])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

