import re
import matplotlib.pyplot as plt
import numpy as np

def parsePing(lines):
    averageMS = []
    overallTime = [[0,0]]
    totalTime = 0
    dataPointRegex = "(\\d+) bytes from (.+): icmp_seq=(\\d+) ttl=(\\d+) time=(.+) ms.*"
    summaryRegex = "(\\d+) packets transmitted, (\\d+) received, (.+)% packet loss, time (\\d+)ms.*"
    for line in lines:
        result = re.search(dataPointRegex, line)
        if result is not None:
            averageMS.append([int(result.group(3)), float(result.group(5))])
            totalTime += float(result.group(5))
            overallTime.append([int(result.group(3)), totalTime])
        else:
            result = re.search(summaryRegex, line)
            #if result is not None:
            #    print(result.groups())
    return [[overallTime, "Ping Sequence Number", "Culmulative Time (ms)"], [averageMS, "Ping Sequence Number", "Time (ms)"]]

def getRate(s):
    #print("Get rate")
    #print(s)
    res = re.search("(.+)([a-zA-Z])", s)
    num = float(res.group(1))
    unit = res.group(2)
    if unit == "B":
        num = num/1024
    elif unit == "M":
        num = num * 1024
    elif unit == "G":
        num = num * 1024 * 1024
    return num

def parseWget(lines):
    averageRate = []
    overallTime = [[0,0]]
    totalTime = 0
    incrementsSec = []
    lengthRegex="Length:\\s+\\d+\\s+\\((\\S)[a-zA-Z]\\).*"
    dataPointRegex = ".+\\d+%\\s+(\\S+\\w) (\\w+)s"
    finalRegex = ".+100%\\s+(\\S+\\w)=(.+)s"
    increments = 0
    expectedLength = 0
    lengthPerIncrement = 50
    roundIncrements = 0
    for line in lines:
        result = re.search(lengthRegex, line)
        if result is not None:
            roundIncrements = 0
            expectedLength = int(result.group(1))
        result = re.search(dataPointRegex, line)
        if result is not None:
            increments+=lengthPerIncrement
            averageRate.append([increments, getRate(result.group(1))])
        else:
            result = re.search(finalRegex, line)
            if result is not None:
                increments+=expectedLength % lengthPerIncrement
                roundIncrements += 1
                averageRate.append([increments, getRate(result.group(1))])
                incrementsSec.append([roundIncrements, float(result.group(2))])
                totalTime += float(result.group(2))
                overallTime.append([roundIncrements, totalTime])
                
    return [[overallTime, "KB downloaded", "Culmulative Time (s)"], [averageRate, "KB downloaded", "Download Speed (KB/s)"], [incrementsSec, "KB downloaded", "Time (s)"]]

def createGraphs(graphs, titles, dir):
    for i in range(len(graphs)):
        graph = graphs[i]
        title = titles[i]
        fileTitle="".join([c for c in list(title) if c.isalnum() or c == ' ']).replace(" ", "_")
        x = np.array([p[0] for p in graph[0]])
        y = np.array([p[1] for p in graph[0]])
        plt.plot(x, y)
        plt.title(title, wrap=True)
        plt.xlabel(graph[1])
        plt.ylabel(graph[2])
        plt.savefig("%s/%s.png" % (dir, fileTitle))
        plt.clf()

def createCombinedGraphs(graphs, titles, dir):
    for i in range(len(titles)):
        title = titles[i]
        graphRef=graphs[0][i]
        fileTitle="".join([c for c in list(title) if c.isalnum() or c == ' ']).replace(" ", "_")
        for g in range(len(graphs)):
            graph=graphs[g][i]
            title = titles[i]
            x = np.array([p[0] for p in graph[0]])
            y = np.array([p[1] for p in graph[0]])
            plt.plot(x, y, label=g)
        plt.title(title, wrap=True)
        plt.xlabel(graphRef[1])
        plt.ylabel(graphRef[2])
        plt.legend()
        plt.savefig("%s/%s.png" % (dir, fileTitle))
        plt.clf()
    print("Len graphs=%d, len titles=%d" % (len(titles), len(graphs)))

if __name__ == "__main__":
    import sys
    command, outputFile = sys.argv[1:3]
    graphTitles = sys.argv[3:]
    graphs = []
    comp = False
    with open(outputFile, "r") as f:
        lines = f.readlines()
        if command == "ping":
            graphs = parsePing(lines)
        elif command == "wget":
            graphs = parseWget(lines)
        elif command == "comparePing":
            section = []
            for l in lines:
                if "@@@@@@@@@@@@" in l:
                    if len(section) > 0:
                        graphs.append(parsePing(section))
                    section = []
                else:
                    section.append(l)
            comp = True
        elif command == "compareWget":
            section = []
            for l in lines:
                if "@@@@@@@@@@@@" in l:
                    if len(section) > 0:
                        graphs.append(parseWget(section))
                    section = []
                else:
                    section.append(l)
            comp = True

    print(graphs)
    if comp:
        createCombinedGraphs(graphs, graphTitles, "./plots")
    else:
        createGraphs(graphs, graphTitles, "./plots")  
