import sys
import re

endOfFileLines = """
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
    print("New link delay update" + link.intf1.name + " t=" + str(time.time()))
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
        print("Updating bw to %f" % randomBandwidth)
        link.intf1.config(bw=randomBandwidth)
        if link.intf1.name not in updatedParams:
            updatedParams[link.intf1.name] = link.intf1.params
        updatedParams[link.intf1.name]["bw"] = str(randomBandwidth)
    elif attribute == "loss":
        link.intf1.config(loss=randomBandwidth)
        if link.intf1.name not in updatedParams:
            updatedParams[link.intf1.name] = link.intf1.params
        updatedParams[link.intf1.name]["loss"] = str(randomBandwidth)
    else:
        if link.intf1.name not in updatedParams:
            updatedParams[link.intf1.name] = link.intf1.params   
    randomTime = random.randint(8, 45)
    scheduler.enter(randomTime, 1, scheduleLinkStateUpdates, [link])


def scheduleTopologyStoring(net, filename):
    print(updatedParams)
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
        print( link.intf1.params, link.intf1.node.name, link.intf1, link.intf1.MAC(), link.intf1.IP(), link.intf2, link.intf2.node.name, link.intf2.MAC(), link.intf2.IP(), link.intf1.params)
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

"""
def run():
    print("injecting integration data")
    filename = sys.argv[1]
    newLines = []
    needsJsonImport = True
    with open(filename, "r") as f:
        lines = f.readlines()
        print("INDESX OF @")
        print(lines.index("#!/usr/bin/env python\n"))
        lines = lines[lines.index("#!/usr/bin/env python\n"):]
        needsJsonImport = True

        for line in lines:
            addSwitch = "(\\w+) = net.addSwitch.+\\)"
            delayMs = ".*{.*'delay':'(\\d+)'}.*"
            endOfConfig = ".*Post configure switches and hosts.*"
            res1 = re.search(addSwitch, line)
            res2 = re.search(endOfConfig, line)
            res3 = re.search(delayMs, line)
            if res1 is not None and 'protocols="OpenFlow10"' not in line:
                newLine = line.rstrip()[:-1] + ', protocols="OpenFlow10")\n'
                newLines.append(newLine)
            elif res2 is not None:
                newLines.append(line)
                break
            elif res3 is not None:
                print("Num is %s" % res3.group(1))
                newLine = line.replace("'delay':'%s'" %  res3.group(1), "'delay':'%sms'" % (res3.group(1)))
                newLines.append(newLine)
            else:
                newLines.append(line)
        if needsJsonImport:
            imports = """
            import json
            import sched
            import time
            import random
            import threading
            import signal
            import sys

            scheduler = sched.scheduler(time.time, time.sleep)

            """.split("\n")
            for l in imports[::-1]:
                newLines.insert(0, '%s\n' % l.strip())
        for line in endOfFileLines.split("\n"):
            newLines.append(line + '\n')
        print(newLines)
    with open(filename, "w") as f:
        for line in newLines:
            f.write(line)
    print("Reformatted file for data collection")




run()