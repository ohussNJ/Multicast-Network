import sys
from socket import socket, AF_INET, SOCK_DGRAM
from tables import routes as globaltable
import packet as p

class Router:

    def __init__(self, nodeid, ip, port):
        self.nodeid = nodeid
        self.ip = ip
        self.port = port
        self.rt = {'neighbors': [{'id':203, 'ip':'192.168.1.4','gateway':'10.0.5.1','port':8883}, {'id':104, 'ip': '192.168.4.1', 'gateway':'192.168.4.2', 'port':8890},],
                   'routes': [{'id':102, 'cost':6, 'route':203}, {'id':103, 'cost':3, 'route':103}, {'id':104, 'cost':1,'route':104}],}

    def search_dst_addr(self, dst):
        for x in range(len(self.rt['neighbors'])):
            if self.rt['neighbors'][x]['id'] == dst:
                return (self.rt['neighbors'][x]['gateway'], self.rt['neighbors'][x]['port'])
        return ('10.0.1.1', 8882)

    def dijkstra(self, graph, src, dest, visited=[], distances={}, predecessors={}):
        """ calculates a shortest path tree routed in src"""
        # a few sanity checks
        if src not in graph:
            raise TypeError('The root of the shortest path tree cannot be found')
        if dest not in graph:
            raise TypeError('The target of the shortest path cannot be found')
            # ending condition
        if src == dest:
            # We build the shortest path and display it
            path = []
            pred = dest
            while pred != None:
                path.append(pred)
                pred = predecessors.get(pred, None)
            p = path[len(path) - 2]
            h = distances[dest]

            global path2
            path2 = path
            return p, h

        else:
            # if it is the initial  run, initializes the cost
            if not visited:
                distances[src] = 0
            # visit the neighbors
            for neighbor in graph[src]:
                if neighbor not in visited:
                    new_distance = distances[src] + graph[src][neighbor]
                    # print(new_distance)
                    if new_distance <= distances.get(neighbor, float('inf')):
                        distances[neighbor] = new_distance
                        predecessors[neighbor] = src
            # mark as visited
            visited.append(src)
            # now that all neighbors have been visited: recurse
            # select the non visited node with lowest distance 'x'
            # run Dijskstra with src='x'
            unvisited = {}
            for k in graph:
                if k not in visited:
                    unvisited[k] = distances.get(k, float('inf'))
            x = min(unvisited, key=unvisited.get)
        return self.dijkstra(graph, x, dest, visited, distances, predecessors)

    # implement heuristic based k out of n algorithm created by Joshua
    def heuristicMulticast(self, pkt, source, k, remk):
        reachable = []
        indices = []
        h = []  # heuristics for each neighbor
        rs = []
        ds = []
        heuristicindices = {}
        # check if destination is immediate neighbor
        for i in self.rt['neighbors']:
            if i['id'] < 200:
                pkttype, seq, length, src, dst, kval, remk, data = p.readDataPacket(pkt)
                remk -= 1
                pkt = p.createDataPacket(seq, self.nodeid, k, i['id'], data, remk)
                server = self.search_dst_addr(i['id'])
                self.handle_sending(pkt, server)
                if remk <= 0:
                    return

        # create list of reachable neighbors without backtracking
        for i in self.rt['neighbors']:
            if i['id'] > 200:
                indices.append(i['id'])
                heuristicindices[i['id']] = 0
                reachable.append(self.reachableDestinations(self.nodeid, i['id']))

        if len(reachable) == 1:
            pkttype, seq, length, src, dst, kval, remk, data = p.readDataPacket(pkt)
            pkt = p.createDataPacket(seq, self.nodeid, k, reachable[0], data, remk)
            server = self.search_dst_addr(indices[0])
            self.handle_sending(pkt, server)
            return
        else:
            # evaluate heuristic for each neighbor
            for i in reachable:
                r = len(i)
                rs.append(r)
                d = self.average_to_reachable_destinations(i, indices[reachable.index(i)])  # calculate d
                ds.append(r)
                j = self.average_to_centroid(self.nodeid, i)  # calculate j
                h.append(r / d)
                heuristicindices[indices[reachable.index(i)]] = r/d
            h = sorted(h,reverse=True)
            maxNode = list(heuristicindices.keys())[list(heuristicindices.values()).index(h[0])]
            counter = 0
            if(len(reachable[indices.index(maxNode)]) < remk):
                while remk > 0:
                    currnode = list(heuristicindices.keys())[list(heuristicindices.values()).index(h[counter])]
                    pkttype, seq, length, src, dst, kval, yee, data = p.readDataPacket(pkt)
                    pkt = p.createDataPacket(seq, self.nodeid, k, currnode, data, remk)
                    server = self.search_dst_addr(currnode)
                    self.handle_sending(pkt, server)
                    remk -= rs[indices.index(currnode)]
                    counter += 1
                return
            else:
                pkttype, seq, length, src, dst, kval, remk, data = p.readDataPacket(pkt)
                pkt = p.createDataPacket(seq, self.nodeid, k, maxNode, data, remk)
                server = self.search_dst_addr(maxNode)
                self.handle_sending(pkt, server)
                return


    #method to send and receive from router in idle state
    def receive(self):
        numretransmissions = 0
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('0.0.0.0', self.port))
        while 1:
            pkt, addr = s.recvfrom(1024)
            print("Received From: ", addr)
            pkttype, seq, length, src, dst, kval, remk, data = p.readDataPacket(pkt)
            if pkttype == 3:
                #ack
                continue
            elif pkttype == 2:
                #data
                #send acknowledge
                #ack = p.createAck(1)
                #s.sendto(ack, addr)
                #multicast the packet
                if kval == 1 or remk == 1:
                    dst = self.findnearestdest()
                    pkt = p.createDataPacket(seq, self.nodeid, 1, dst, data, 1)
                    server = self.search_dst_addr(dst)
                    self.handle_sending(pkt, server)
                    continue
                else:
                    pkt = p.createDataPacket(seq, self.nodeid, 1, dst, data, 1)
                    self.heuristicMulticast(pkt,src, kval, remk)
                    continue

            elif pkttype == 1:
                #update
                #lspkt = p.readLSpkt(pkt)
                continue
            elif pkttype == 0:
                #hellopkt = p.readHellopkt(pkt)
                continue

    # Sends packet to dst address
    def handle_sending(self, packet, server):
        s = socket(AF_INET, SOCK_DGRAM)
        s.sendto(packet, server)
        print('Sending To: ', server)
        s.close()
        return 0

    def findByid(self,id,l):
        for i in l:
            if i['id'] == id:
                return i
        return id

    def findnearestdest(self):
        fdst = 0
        min = 100
        for i in self.rt['routes']:
            if i['id'] >= 200:
                continue
            else:
                if i['cost'] < min:
                    min = i['cost']
                    #print(i['id'])
                    dest = self.findByid(i['id'],self.rt['routes'])
                    fdst = dest['route']
                    #print(dest)
                    #print(fdst)
        return fdst


    """
    def isNeighbor(self, neighbor):
        for i in hD.RoutingTables.get(self.nodeid):
            if i == neighbor:
                return True
        return False
    """

    #find if a list of lists is all equal
    def sameLists(self, l):
        for i in range(len(l)):
            tmp = l[i]
            j = len(l) - i - 1
            while j < len(l)-1:
                if set(l[i]) != set(l[j]):
                    return False
                j += 1
        return True

    #helper function for finding r
    def reachableDestinations(self, source, nodeid):
        nodeDests = globaltable[str(nodeid)]['routes']
        r = []
        for i in nodeDests:
            if i['route'] == source:
                continue
            else:
                r.append(i['id'])
        return r

    #helper function for finding j
    def average_to_reachable_destinations(self, destinations, nodeid):
        den = len(destinations)
        cost = 0
        for i in destinations:
            dests = globaltable[str(nodeid)]['routes']
            for j in dests:
                if j['id'] in destinations:
                    cost += j['cost']

        return cost/den
    #helper function for finding d
    def average_to_centroid(self, source, nodeid):
        return 0

if __name__ == '__main__':
    print("Router Started...")
    r = Router(205,'192.168.5.3',8885)
    r.receive()