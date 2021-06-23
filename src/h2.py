from socket import socket, AF_INET, SOCK_DGRAM
import packet as p

#Creates to new server
class udpserver():

        def __init__(self, id, ip, gateway, port):
                self.ip = ip
                self.id = id
                self.default_gateway = gateway
                self.port = port

        def receive_packet(self, h, sent_packet):
            s = socket(AF_INET, SOCK_DGRAM)
            s.bind(('0.0.0.0', h.port))

            while True:
                packet, addr = s.recvfrom(1024)
                pkttype, seq, length, src, dst, kval, remk, data = p.readDataPacket(packet)
                if pkttype == 2:
                    print("Received: " + data + "From " + str(src))
#Initializes new server and sets it up to receive packets
if __name__ == '__main__':
        print("Server Start...")
        udp_server = udpserver(id=103, ip='192.168.3.1', gateway=('192.168.3.2',8884), port=8889)
        udp_server.receive_packet(udp_server, None)
