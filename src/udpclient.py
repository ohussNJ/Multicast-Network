from socket import socket, AF_INET, SOCK_DGRAM
import packet as p


# Creates class for client
class udpclient():
    def __init__(self, id, ip, gateway, port):
        self.ip = ip
        self.id = id
        self.default_gateway = gateway
        self.port = port
        self.rt = {'neighbors': [{'id': 201, 'ip': '192.168.1.2', 'gateway': '192.168.1.1', 'port': 8881}],
                   'routes': [{'id': 102, 'cost': 4}, {'id': 103, 'cost': 3}, {'id': 104, 'cost': 3}]}

        # Sends packet to dst address

    def handle_sending(self, packet, server):
        s = socket(AF_INET, SOCK_DGRAM)
        s.sendto(packet, server)
        print('Sending To: ', server)
        s.close()
        return 0


# Initializes a new client and starts the ping
if __name__ == '__main__':
    udp_client = udpclient(id=101, ip='192.168.1.1', gateway=('192.168.1.2', 8881), port=8880)
    k = int(input("Enter k:"))
    #print(type(udp_client.id))
    packet = p.createDataPacket(1,udp_client.id,k,0,"Final Project",k)
    neighbor = (udp_client.rt['neighbors'][0]['id'], udp_client.rt['neighbors'][0]['id'])
    udp_client.handle_sending(packet, udp_client.default_gateway)
    print("Transmitting ", packet, "to ", udp_client.default_gateway)
