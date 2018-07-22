

import struct
import socket
import time
from ctypes import *


class IP(Structure):
    _fields_ = [("version", c_ubyte, 4),
                ("ihl", c_ubyte, 4),
                ("tos", c_ubyte),
                ("length", c_ushort),
                ("ident", c_ushort),
                ("offset", c_ushort),
                ("ttl",  c_ubyte),
                ("protocol", c_ubyte),
                ("checksum", c_ushort),
                ("src", c_long),
                ("dst", c_long)]

    def __new__(self, socket_buffer = None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer = None):
        self.src_address = socket.inet_ntoa(struct.pack("@I", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("@I", self.dst))
        self.id = struct.unpack("<H", struct.pack(">H", self.ident))

class ICMP(Structure):
    _fields_ = [("typ", c_ubyte),
                ("code", c_ubyte),
                ("checksum", c_ushort),
                ("identity", c_ushort),
                ("sequence", c_ushort)]

    def __new__(self, socket_buffer = None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer = None):
        self.check = struct.unpack("<H", struct.pack(">H", self.checksum))

def send_packet(socket, dst):
    typ = 8
    code = 0
    check = 29158
    ident = 5656
    seq = 1
    payload = b'pls send me a icmp reply packet!'

    icmpPack = struct.pack('!BBHHHs', typ, code, check, ident, seq, payload)
    sock.sendto(icmpPack, (dst, 1))
    send_time = time.time()

    recv_time, reply = recv_packet(socket)

    return  recv_time, reply, send_time

def recv_packet(socket):
    try:
        reply = socket.recv(1024)
    except socket.timeout:
        reply = "timed out"
    recv_time = time.time()

    return recv_time, reply

dst = '8.8.8.8'
sent_count = 0
success_count = 0
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

print("Pinging " + dst + " with 32 bytes of data:\n")

for c in range(0, 4):
    sock.settimeout(4.0)
    recv_time, reply, send_time = send_packet(sock, dst)
    sock.settimeout(0)
    sent_count += 1

    ip = IP(reply[:20])
    icmp = ICMP(reply[20:28])
    round_time = round((recv_time - send_time)*1000)

    if(icmp.typ == 0):
        print("Reply from " + ip.src_address + " bytes=32 time=" + str(round_time) + "ms TTL=" + str(ip.ttl))
        success_count += 1
    elif(icmp.typ == 3):
        print("Reply from " + ip.src_address + ": Destination host unreachable")
    elif(reply == "timed out"):
        print("Request timed out")
    time.sleep(1)


lost_count = sent_count - success_count
print("\nPing statistics for " + dst + ":")
print("\tSent = " + str(sent_count) + ", Recieved = " + str(success_count) + ", Lost = " + str(lost_count) + " (" + str(((100/sent_count)*lost_count)) + "%)")

#functional request  and reply. format output!! DONE BANSAAII!!!
#Reply from <dst_address> bytes=32 time=<time_ms> TTL=<ttl_ip_header> DONE BANSAAAAI!!
#Set time out DONE BANSAAAI!!!!
#Checksum calculator
#Ping destination IP by input