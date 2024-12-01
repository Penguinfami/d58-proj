import random

class ShortestPathsAlgorithm:

    def __init__(self):
        self.nodes = set()
        self.edges = set()
        self.routingTable = dict()
        self.forwardingTable = dict()

    def computePath(self, algorithm, attr, comp):
        print("Sorting by " + attr)
        if algorithm == "dijkstra":
            self.djikstra(attr, comp)
        elif algorithm == "st":
            self.spanning(attr)
        elif algorithm == "mst":
            self.kruskal(attr, comp)
        else: 
            print("Invalid sorting" + algorithm)

    def addNode(self, node):
        curNames = [n.name for n in self.nodes]
        if node.name not in curNames:
            self.nodes.add(node)

    def addEdge(self, edge):
        curEdges = [(e.start.name, e.end.name) for e in self.edges]
        if (edge.start.name, edge.end.name) not in curEdges:
            self.edges.add(edge)

    def reset(self):
        self.nodes = set()
        self.edges = set()

    def findEdge(self, node1, node2):
        for e in self.edges:
            if e.start.name == node1 and e.end.name == node2:
                return e
            elif e.start.name == node2 and e.end.name == node1:
                return e
        return None

    def findNode(self, name):
        for n in self.nodes:
            if n.name == name:
                return n
        return None
    
    def getNextInPath(self, start, end):
        return self.forwardingTable[start][end]

    def djikstra(self, attr, comp):
        allEdges = set([(e.start.name, e.end.name) for e in self.edges])
        allNames = set([n.name for n in self.nodes])
        print(allNames)
        noneValue = -1
        for startNode in self.nodes:
            # attr = what to sort by, ex: delay, bandwidth
            S = set()
            S.add(startNode.name)
            D = {}
            EdgesUsed = {}
            T = set()
            orderedT = set()
            for node in self.nodes:
                theoreticalAdjacentEdge1 = (node.name, startNode.name)
                theoreticalAdjacentEdge2 = (startNode.name, node.name)
                if theoreticalAdjacentEdge1 in allEdges or theoreticalAdjacentEdge2 in allEdges:
                    adjacentEdge = self.findEdge(node.name, startNode.name)
                    D[node.name] = adjacentEdge.props[attr]
                    EdgesUsed[node.name] = adjacentEdge
                else:
                    D[node.name] = noneValue
            while len(S) < len(allNames):
                nodesNotInSNames = allNames.difference(S)
                smallestDist = 999999999999
                smallestNodeName = None
                for n in nodesNotInSNames:
                    if D[n] >= 0 and (D[n] < smallestDist):
                        smallestDist = D[n]
                        smallestNodeName = n
                S.add(smallestNodeName)
                T.add(EdgesUsed[smallestNodeName])
                orderedT.add((EdgesUsed[smallestNodeName].start.name if  EdgesUsed[smallestNodeName].start.name != smallestNodeName else  EdgesUsed[smallestNodeName].end.name,smallestNodeName))
                for n in nodesNotInSNames:
                    possibleAdjacent = self.findEdge(smallestNodeName, n)
                    if possibleAdjacent is not None and n != smallestNodeName:
                        newAttrValue = possibleAdjacent.props[attr]
                        #print("Attr value for adjacent %s and %s = %f" % (n, smallestNodeName, newAttrValue))
                        if D[n] == noneValue or (D[n] > D[smallestNodeName] + newAttrValue):
                            D[n] = D[smallestNodeName] + newAttrValue
                            EdgesUsed[n] = possibleAdjacent
            self.routingTable[startNode.name] = T
            self.createForwardingTableFromShortestPaths(orderedT, startNode.name)

    # Function to perform DFS and detect cycles in the graph
    def dfs(self, node, visited, parent, edges):
        visited.add(node)  # Mark the current node as visited
        
        # Traverse all edges and check for cycles
        for edge in edges:
            # Skip the edges where node is not one of the ends
            if edge.start.name == node:
                neighbor = edge.end.name
            elif edge.end.name == node:
                neighbor = edge.start.name
            else:
                continue  # Ignore edges that do not involve the current node
            
            # If the neighbor has not been visited, do a DFS from it
            if neighbor not in visited:
                if self.dfs(neighbor, visited, node, edges):
                    return True
            # If the neighbor is visited and it's not the parent, a cycle is detected
            elif neighbor != parent:
                return True
        return False

    # Function to check if the graph contains a cycle
    def has_cycle(self, nodes, edges):
        visited = set()  # Set to keep track of visited nodes
        # Call DFS for each unvisited node
        for node in nodes:
            if node not in visited:
                if self.dfs(node, visited, None, edges):  # Start DFS from the node
                    return True  # Cycle detected
        return False  # No cycle detected

    def kruskal(self, attr, comp):
        allEdges = set([(e.start.name, e.end.name) for e in self.edges])
        allNames = set([n.name for n in self.nodes])
        allEdgesSorted = self.edges
        allEdgesSorted = sorted(allEdgesSorted, key=lambda x: x.props[attr])
        if comp == "max":
            allEdgesSorted = allEdgesSorted[::-1]
        print("Sorted edges")
        print(allEdgesSorted)
        print(allEdgesSorted[0].props[attr])
        print(allEdgesSorted[-1].props[attr])
        spanningTree = []
        print("%d total nodes" % len(allNames))
        print(allNames)
        nodesIncluded = set()
        while len(spanningTree) < len(allNames) - 1:
            smallestEdge = allEdgesSorted[0]

            nodesIncluded.add(smallestEdge.start.name)
            nodesIncluded.add(smallestEdge.end.name)

            if not self.has_cycle(nodesIncluded, spanningTree + [smallestEdge]):
                spanningTree.append(smallestEdge)
                print("Added (%s, %s) to spanning tree" % (smallestEdge.start.name, smallestEdge.end.name))
            else:
                print("A cycle is formed by (%s %s)" % (smallestEdge.start.name, smallestEdge.end.name))

            allEdgesSorted = allEdgesSorted[1:]
            print([(e.start.name, e.end.name) for e in allEdgesSorted])
            print([(e.start.name, e.end.name) for e in spanningTree])

            print(len(spanningTree))
        for n in self.nodes:
            self.createForwardingTableFromSpanningTree([(e.start.name, e.end.name) for e in spanningTree], n.name)
    
    def spanning(self, attr):
        allEdges = set([(e.start.name, e.end.name) for e in self.edges])
        allNames = set([n.name for n in self.nodes])
        allEdgesSorted = list(self.edges)
        random.shuffle(allEdgesSorted)#allEdgesSorted = sorted(allEdgesSorted, key=lambda x: x.props[attr])
        print("Sorted edges")
        print(allEdgesSorted)
        print(allEdgesSorted[0].props[attr])
        print(allEdgesSorted[-1].props[attr])
        spanningTree = []
        print("%d total nodes" % len(allNames))
        print(allNames)
        nodesIncluded = set()
        while len(spanningTree) < len(allNames) - 1:
            smallestEdge = allEdgesSorted[0]

            nodesIncluded.add(smallestEdge.start.name)
            nodesIncluded.add(smallestEdge.end.name)

            if not self.has_cycle(nodesIncluded, spanningTree + [smallestEdge]):
                spanningTree.append(smallestEdge)
                print("Added (%s, %s) to spanning tree" % (smallestEdge.start.name, smallestEdge.end.name))
            else:
                print("A cycle is formed by (%s %s)" % (smallestEdge.start.name, smallestEdge.end.name))

            allEdgesSorted = allEdgesSorted[1:]
            print([(e.start.name, e.end.name) for e in allEdgesSorted])
            print([(e.start.name, e.end.name) for e in spanningTree])

            print(len(spanningTree))
        for n in self.nodes:
            self.createForwardingTableFromSpanningTree([(e.start.name, e.end.name) for e in spanningTree], n.name)    
    
    def createForwardingTableFromShortestPaths(self, orderedT, startNode):
        F = {}
        adjacentEdges = [e[1] for e in orderedT if e[0] == startNode]
        for adjacentEdge in adjacentEdges:
            F[adjacentEdge] = adjacentEdge
            curStart = [adjacentEdge]
            while len(curStart) > 0:
                nextLinks = [e[1] for e in orderedT if e[0] in curStart]
                for nextLink in nextLinks:
                    F[nextLink] = adjacentEdge
                curStart = nextLinks
        print("Created forwarding table for " + startNode)
        print(F)
        print(orderedT)
        self.forwardingTable[startNode] = F

    def createForwardingTableFromSpanningTree(self, tree, startNode):
        F = {}
        adjacentEdges = set([e[1] for e in tree if e[0] == startNode] + [e[0] for e in tree if e[1] == startNode])
        reachedEdges = [x for x in adjacentEdges]
        for adjacentEdge in adjacentEdges:
            F[adjacentEdge] = adjacentEdge
            curStart = [adjacentEdge]
            while len(curStart) > 0:
                nextLinks = [e[1] for e in tree if e[0] in curStart and e[1] not in reachedEdges] + [e[0] for e in tree if e[1] in curStart and e[0] not in reachedEdges] 
                for nextLink in nextLinks:
                    F[nextLink] = adjacentEdge
                curStart = nextLinks
                reachedEdges.extend(curStart)
                print(curStart)
        print("Created forwarding table for " + startNode)
        print(F)
        print(tree)
        self.forwardingTable[startNode] = F
class Node:
    def __init__(self, name, props={}):
        print("Creating node with name =%s" % name)
        self.name = name
        self.props = props

class Edge:
    def __init__(self, node1, node2, props={}):
        print("Creating edge with props = ", props)
        self.start = node1
        self.end = node2
        self.props = props


def demo():
    edges = [
        ("u", "v",3),
        ("u", "w", 2),
        ("v","y", 2),
        ("v", "x", 1),
        ("w", "x", 1),
        ("w", "s", 4),
        ("x", "t", 5),
        ("x", "z", 4),
        ("y", "z", 1),
        ("s", "t", 3)
    ]
    nodes = list("uvwsxtyz")
    alg = ShortestPathsAlgorithm()
    print(len(nodes))
    for n in nodes:
        newNode = Node(n)
        alg.addNode(newNode)

    for e in edges:
        props = {}
        props["weight"] = e[2]
        print("Creating edge with nodes %s and %s: " % (e[0], e[1]))
        newEdge = Edge(alg.findNode(e[0]), alg.findNode(e[1]), props)
        alg.addEdge(newEdge)
    alg.computePath("weight")
