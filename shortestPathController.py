from pox.core import core
from pox.host_tracker import host_tracker
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import EventMixin
from pox.lib.packet import ethernet, ipv4
from shortestPathsAlgorithm import ShortestPathsAlgorithm, Node, Edge
from pox.openflow.discovery import Discovery, LinkEvent
from pox.topology import topology
import pox.lib.packet.arp as arp
from projectnetwork import myNetwork
from pox.lib.addresses import EthAddr, IPAddr
import re
import json
import sys
import sched
import time
import threading
import signal

log = core.getLogger()
scheduler = sched.scheduler(time.time, time.sleep)

delay = 1
capacity = 100

sortingAttribute = "w"
routingAlgorithm = "w"
sortingAttributeShortest = "w"

scheduledEvents = []


def handle_ctrl_c(signal, frame):
    print("Ctrl-C pressed. Stopping Controller...")
    for e in scheduledEvents:
        scheduler.cancel(e)
    core.quit() 
    sys.exit(0)  

class ShortestPathController(EventMixin):

    def __init__(self):
        print("Init controller")
        log.debug("Initing")
        log.debug(str(sys.argv))
        self.switches = []
        self.arp_table = {}
        self.macToInterface = {}
        self.linkPorts = {}
        self.computingBlocked = False
        log.info("IP-to-MAC mapping initialized")
        self.routing = ShortestPathsAlgorithm()
        log.info("Setting up listeners")
        core.openflow.addListeners(self)
        core.openflow_discovery.addListeners(self)
        self.loadNetworkData()
        scheduler_thread = threading.Thread(target=self.schedule_events)
        scheduler_thread.daemon = True
        scheduler_thread.start()
    
    def schedule_events(self):
        scheduler.enter(5, 1, self.loadUpdatedNetworkData, [])
        scheduler.run()

    def loadNetworkData(self):
        print("Loading network data")
        self.computingBlocked = True

        with open("/home/mininet/cs144_lab3/pox_module/project/networkdata.json", "r") as f:
            data = json.load(f)
            #print(data)
            for link in data["links"]:
                startName = str(link[u'startName'])
                endName = str(link[u'endName'])
                startInterface = str(link[u'startInterface'])
                endInterface = str(link[u'endInterface'])
                startNode = Node(startName)
                endNode = Node(endName)
                props = {}
                print("Getting params")
                params = link[u'params']
                print(params)
                for key in params:
                    print(key)
                    numeric = int(re.sub('\\D', '', str(params[str(key)])))
                    props[str(key)] = numeric if core.sortingAttributeShortest == "min" else 99999999 - numeric
                print("Creating edge")
                print(props)
                edge = Edge(startNode, endNode, props)
                self.routing.addNode(startNode)
                self.routing.addNode(endNode)
                self.routing.addEdge(edge)
                startMAC = link[u'startMAC']
                endMAC = link[u'endMAC']
                startIP = link[u'startIP']
                endIP = link[u'endIP']
                if startIP is not None:
                    self.arp_table[str(startIP)] = str(startMAC)
                if endIP is not None:
                    self.arp_table[str(endIP)] = str(endMAC)
                self.macToInterface[str(startMAC)] = {
                    "interface": startInterface,
                    "node": str(data["interfaces"][startInterface][u"node"]),
                }
                self.macToInterface[str(endMAC)] = {
                    "interface": endInterface,
                    "node": str(data["interfaces"][endInterface][u"node"]),
                }
                if startName not in self.linkPorts:
                    self.linkPorts[startName] = {}

                self.linkPorts[startName][endName] = {
                    "port": int(link[u'startPort']),
                    "startInterface": startInterface,
                    "endInterface": endInterface
                }
                if endName not in self.linkPorts:
                    self.linkPorts[endName] = {} 
                self.linkPorts[endName][startName] = {
                    "port": int(link[u'endPort']),
                    "startInterface": endInterface,
                    "endInterface": startInterface
                }
    
        #print("Attr is ", core.sortingAttribute)
        self.routing.computePath(core.routingAlgorithm, core.sortingAttribute, core.sortingAttributeShortest)
        self.computingBlocked = False

    def loadUpdatedNetworkData(self):
        print("Loading updated data")
        with open("/home/mininet/cs144_lab3/pox_module/project/networkdata.json", "r") as f:
            data = json.load(f)
            #print(data)
            self.computingBlocked = True

            self.routing.reset()

            for link in data["links"]:
                startName = str(link[u'startName'])
                endName = str(link[u'endName'])
                startInterface = str(link[u'startInterface'])
                endInterface = str(link[u'endInterface'])
                startNode = Node(startName)
                endNode = Node(endName)
                props = {}
                print("Getting params")
                params = link[u'params']
                for key in params:
                    print(params)
                    numeric = int(re.sub('\\D', '', str(params[str(key)])))
                    props[str(key)] = numeric
                edge = Edge(startNode, endNode, props)
                self.routing.addNode(startNode)
                self.routing.addNode(endNode)
                self.routing.addEdge(edge)

        print("Computing new shortest paths")
        self.routing.computePath(core.routingAlgorithm, core.sortingAttribute, core.sortingAttributeShortest)
        self.computingBlocked = False

        scheduler.enter(15, 1, self.loadUpdatedNetworkData, [])
                
    def _handle_HostEvent(self, event):
        log.info("HOST EVENT!")
        log.debug("****************************************")
        sys.exit()
        if event.added:
            host = event.host
            ip = host.IP()  # Get host IP
            mac = host.MAC()  # Get host MAC
            self.arp_table[ip] = mac  # Store the IP-MAC mapping
            log.debug("Host added: IP %s, MAC %s", ip, mac)

    def _handle_LinkEvent(self, event):
        #print("Link event here")
        # link added/removed
        link = event.link
        #(dir(link))
        if event.added:
            #log.debug(link.keys)
            #log.debug(link.values())
            log.debug("Added switch from ")
            log.debug(dir(link))
            log.debug("Link between switch %s and switch %s on ports %s and %s" % 
                (link.dpid1, link.dpid2, link.port1, link.port2))
            log.debug(dir(event))
            



    def _handle_PacketIn(self, event):
        packet = event.parsed
        #print("Handle packet from src=%s to %s, dpid1=%d" % (packet.src, packet.dst, event.dpid))
        #print(dir(packet))
        #print("Packet type: %s", type(packet))  # See the type of the outer packet
        #print("Packet payload type: %s", type(packet.payload))  # See the type of the payload
        # Example: Forward packet to a specific port
               
        while self.computingBlocked:
            print("Waiting....")

        if isinstance(packet, ethernet) and isinstance(packet.payload, ipv4):
            ip_packet = packet.next
            #print("IPv4: src=%s, dst=%s, proto=%s " % (ip_packet.srcip, ip_packet.dstip, ip_packet.protocol))
            #print(self.macToInterface)
            etherSourceNode=self.macToInterface[str(packet.src)]["node"]
            etherTargetNode=self.macToInterface[str(packet.dst)]["node"]
            #print("ETHER src=%s dst=%s" % (etherSourceNode, etherTargetNode))
            #print(self.macToInterface)
            sourceNode=self.getNodeFromIp(ip_packet.srcip)
            targetNode=self.getNodeFromIp(ip_packet.dstip)
            #print("IP src=%s dst=%s" % (sourceNode, targetNode))
            ##print(self.forwardingTable[etherSourceNode])
            theoreticalSrcNextHop = self.routing.getNextInPath(etherSourceNode, targetNode)
            theoreticalSrcMAC = self.getMACFromNode(theoreticalSrcNextHop)
            if theoreticalSrcNextHop != etherTargetNode:
                nextHop = self.routing.getNextInPath(theoreticalSrcNextHop, targetNode)
                srcNode = theoreticalSrcNextHop
            elif etherTargetNode != targetNode:
                nextHop = self.routing.getNextInPath(etherTargetNode, targetNode)
                srcNode = etherTargetNode
            else:
                nextHop = targetNode
                srcNode = etherSourceNode
                #print("WHAT NOW???????????")
            #print(self.arp_table)
            #print("Getting macs from interfaces")
            srcMac = self.getMACFromInterface(self.linkPorts[srcNode][nextHop]["startInterface"])

            outgoingPort = self.linkPorts[srcNode][nextHop]["port"]

            #print("Srcmac=%s nexthop=%s" % (self.macToInterface[srcMac], nextHop))
            
            nextMAC = self.getMACFromInterface(self.linkPorts[srcNode][nextHop]["endInterface"])
            #print("Dst node=%s Src node=%s" % (targetNode,sourceNode))
            #print("Nexthop=%s, nexthop mac=%s" % (nextHop, nextMAC))
            ether_forward = ethernet(dst=EthAddr(nextMAC), src=EthAddr(srcMac), type=ethernet.IP_TYPE)
            ether_forward.set_payload(ip_packet)
            ofp = of.ofp_packet_out()
            #print(self.linkPorts)
            #print("Outing node=%s, nexthop=%s" % (etherTargetNode, nextHop))
            ofp.actions.append(of.ofp_action_output(port=outgoingPort))
            #print("Sending IP reply on to port ", event.port, outgoingPort)
            #print("Sending packet with macs src=%s, dst=%s" % (srcMac, nextMAC))
            ofp.data = ether_forward.pack()
            event.connection.send(ofp)

            
        # Check if the packet is Ethernet and its payload is ARP
        if isinstance(packet, ethernet) and isinstance(packet.payload, arp):
            arp_packet = packet.payload  # Access the ARP packet
            print("ARP: src_mac=%s, dst_mac=%s, op=%s" % (arp_packet.hwsrc, arp_packet.hwdst, arp_packet.opcode))

            # Check if it's an ARP request
            if arp_packet.opcode == arp.REQUEST:
                #print("Received ARP Request from %s" % arp_packet.hwsrc)

                # If the requested IP is in our "known" IP-to-MAC mapping
                requested_ip = arp_packet.protodst  # This is the IP that the request is asking for
                #print("ARP Request for IP: %s" % requested_ip)
                #print("OR IS IT %s " % arp_packet.protodst)
                #print("ARP TABLE")
                #print(self.arp_table)
                #print(type(arp_packet.protosrc))
                #print("MAC TO INTERFACE")
                #print(self.macToInterface)
                #print("10.0.0.1" in self.arp_table)
                #print(str(requested_ip) in self.arp_table)
                if str(requested_ip) in self.arp_table:
                    # We found a matching MAC address for the requested IP
                    mac_address = self.arp_table[str(requested_ip)]

                    # Construct an ARP reply packet
                    arp_reply = arp(opcode=arp.REPLY,
                                        hwsrc=EthAddr(mac_address), hwdst=EthAddr(arp_packet.hwsrc),
                                        protosrc=IPAddr(requested_ip), protodst=IPAddr(arp_packet.protosrc))

                    # Send the ARP reply back to the switch
                    ether_reply = ethernet(dst=EthAddr(packet.src), src=EthAddr(mac_address), type=ethernet.ARP_TYPE)
                    ether_reply.set_payload(arp_reply)

                    # Send the packet out through the switch (port is found in event of packet_in)
                    ofp = of.ofp_packet_out()
                    ofp.actions.append(of.ofp_action_output(port=event.port))
                    #print("Sending ARP reply on port ", event.port)
                    ofp.data = ether_reply.pack()
                    event.connection.send(ofp)

                    #print("Sent ARP Reply: %s is at %s", requested_ip, mac_address)
                else:
                    ""
                    #print("No MAC address found for requested IP %s", requested_ip)
        #nexthop = self.routing.getNextInPath(ip_packet.srcip, ip_packet.dstip)

    def getNodeFromIp(self, ip):
        ipMAC = self.arp_table[str(ip)]
        for mac in self.macToInterface:
            if mac == ipMAC:
                return self.macToInterface[mac]["node"]
        return None 
    def getMACFromInterface(self, iface):
        for mac in self.macToInterface:
            if self.macToInterface[mac]["interface"] == iface:
                return mac
        return None 
    def getMACFromNode(self, node):
        for mac in self.macToInterface:
            if self.macToInterface[mac]["node"] == node:
                return mac
        return None 

def launch(attribute="delay", shortest="min", routing="djikstra"):
    log.debug("Registering new controller")
    #print(attribute)
    print("?DSFSDFDSF")
    print(attribute)
    print(shortest)
    print(routing)

    sortingAttribute=attribute
    core.sortingAttributeShortest=shortest
    core.routingAlgorithm=routing
    #from host_tracker import launch
    #launch()
    print("????????????")
    signal.signal(signal.SIGINT, handle_ctrl_c)

    # Delay setup until host_tracker is ready
    core.sortingAttribute = attribute
    core.registerNew(ShortestPathController)
    #net = myNetwork()
    ##print("NET")
    ##print(dir(net))
