# K-out-of-N-Multicast-Protocol
* This project creates a multicast protocol to efficiently send the same packet to multiple hosts within a local network.

## Table of contents
* [General info](#general-info)
* [Routing Algorithm](#routing-algorithm)
* [Multicast Algorithm](#mutlicast-algorithm)
* [Algorithms for Message Forwarding](#algorithms-for-message-forwarding)
* [Setup](#setup)
* [Demo](#demo)

## General info
* A message is sent from one sender to 1-3 recipients
* Each packet will have n= 1, 2, or 3 destinations
* Multicast message to “best k (=<n)” destinations
* Routing protocol chooses the ‘best’ multicast path
* A complete design overview is available [here](https://drive.google.com/file/d/1Kzl9Lt64VvcNXFhre3tpvDGES9K7YGHu/view?usp=sharing).
	
## Routing Algorithm
* The Protocol uses a Link State routing algorithm using Open Shortest Path First (OSPF) and Dijkstra’s algorithm to construct routing tables.
* Each node performs a Dijkstra operation to find the shortest path to any node. The routing table has an entry for every other node (both routers and sources) in the topology, and the 
entries include: the distance to that node, the next-hop required to get to that node, and the second to last hop to get to that node.

## Mutlicast Algorithm
* A lookahead heuristic to minimize the number of casts used to reach all k nodes.
* The presence of the second to last hop in the routing table allows this lookahead to be virtual, without the need for additional packet transfer. Once each destination’s shortest path 
to the router is known, these paths are compared to find the closest centroid router for all given destinations.

## Algorithms for Message Forwarding
* When the data forwarding plane sends a packet down a path, as determined by the routing algorithm, it uses a simple copy and forward method. However, when the algorithm reaches a 
diverging point, the packets sent down the different paths will vary in the K-remaining field. For different paths the number of packets sent will be exact matches to the number needed.
	
## Setup
* Copy Python scripts and the given topology
* Execute topology python script using Mininet to create a topology
* Verify the topology using ping commands from the host to destinations
* xterm all given nodes
* Execute the corresponding router script for each router
* Execute the corresponding host script for each host 
* Execute UDPClient.py on source node 

## Demo
This demo runs on the following topology:
* ![Screenshot (150)](https://user-images.githubusercontent.com/76886099/117210183-5ae43580-adc5-11eb-9514-7ee4a46e503b.png)
* Unicast (k=1)
![Screenshot (153)](https://user-images.githubusercontent.com/76886099/117227521-fdf87780-ade4-11eb-97b5-1c8e4b2c0b6a.png)
* Multicast (k=2, k=3)
![Screenshot (154)](https://user-images.githubusercontent.com/76886099/117227658-5af42d80-ade5-11eb-9934-0e3f20c53854.png)
