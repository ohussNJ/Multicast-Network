# Comnetsii APIs for Packet. Rutgers ECE423/544
# Author: Fares Elkhouli, Omar Hussein
import struct
import random


# TTL is omitted in all packets

# ommited n-val
def createDataPacket(seq, src, kval, dst, data, remK):
    """Create a new packet based on given id"""
    pktlen = len(data)
    header = struct.pack('BBBBBBB', 2, seq, pktlen, src, dst, kval, remK)
    return header + bytes(data, 'utf-8')


def readDataPacket(pkt):
    n = struct.calcsize('BBBBBBB')
    header = pkt[0:n]
    data = pkt[n:]
    pkttype, seq, length, src, dst, kval, remk = struct.unpack('BBBBBBB', header)
    return pkttype, seq, length, src, dst, kval, remk, str(data, 'utf-8')


def createLSpkt(src, lsData):
    seq = random.randint(0, 254)
    header = struct.pack('BBB', 1, seq, src)
    return header + bytes(lsData, 'utf-8')


def readLSpkt(pkt):
    n = struct.calcsize('BBB')
    header = pkt[0:n]
    data = pkt[n:].decode('utf-8')
    pkttype, seq, src = struct.unpack('BBB', header)
    return pkttype, seq, src, data


def createAck(seq):
    return struct.pack("BB", 3, seq)


def readAck(pkt):
    pkttype, seq = struct.unpack('BB', pkt)
    return pkttype, seq


def createHellopkt(seq, src):
    return struct.pack("BBL", 0, seq, src)


def readHellopkt(pkt):
    n = struct.calcsize('BBL')
    header = pkt[0:n]
    pkttype, seq, src = struct.unpack('BBL', header)
    return pkttype, seq, src
