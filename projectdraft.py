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
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s13 = net.addSwitch('s13', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s16 = net.addSwitch('s16', cls=OVSKernelSwitch)
    s12 = net.addSwitch('s12', cls=OVSKernelSwitch)
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
    s9 = net.addSwitch('s9', cls=OVSKernelSwitch)
    s14 = net.addSwitch('s14', cls=OVSKernelSwitch)
    s10 = net.addSwitch('s10', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s11 = net.addSwitch('s11', cls=OVSKernelSwitch)
    s15 = net.addSwitch('s15', cls=OVSKernelSwitch)
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.21', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.22', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.23', defaultRoute=None)

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
    net.get('s5').start([c0])
    net.get('s13').start([c0])
    net.get('s4').start([c0])
    net.get('s1').start([c0])
    net.get('s16').start([c0])
    net.get('s12').start([c0])
    net.get('s7').start([c0])
    net.get('s6').start([c0])
    net.get('s9').start([c0])
    net.get('s14').start([c0])
    net.get('s10').start([c0])
    net.get('s3').start([c0])
    net.get('s11').start([c0])
    net.get('s15').start([c0])
    net.get('s8').start([c0])
    net.get('s2').start([c0])

    info( '*** Post configure switches and hosts\n')
    s5.cmd('ifconfig s5 10.0.0.5')
    s13.cmd('ifconfig s13 10.0.0.13')
    s4.cmd('ifconfig s4 10.0.0.4')
    s1.cmd('ifconfig s1 10.0.0.1')
    s16.cmd('ifconfig s16 10.0.0.16')
    s12.cmd('ifconfig s12 10.0.0.12')
    s7.cmd('ifconfig s7 10.0.0.8')
    s6.cmd('ifconfig s6 10.0.0.6')
    s9.cmd('ifconfig s9 10.0.0.9')
    s14.cmd('ifconfig s14 10.0.0.14')
    s10.cmd('ifconfig s10 10.0.0.10')
    s3.cmd('ifconfig s3 10.0.0.3')
    s11.cmd('ifconfig s11 10.0.0.11')
    s15.cmd('ifconfig s15 10.0.0.15')
    s8.cmd('ifconfig s8 10.0.0.8')
    s2.cmd('ifconfig s2 10.0.0.2')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

