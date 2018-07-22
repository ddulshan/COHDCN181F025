import struct
import socket
import time
import sys
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

def send_packet(sock, dst):
    typ = 8
    code = 0
    check = 0
    ident = 5656
    seq = 1
    payload = 0

    dummy_icmpPack = struct.pack('BBHHHb', typ, code, check, ident, seq, payload)
    check = (checksum(str(dummy_icmpPack)[2:-1])) - 6693
    icmpPack = struct.pack('!BBHHHb', typ, code, check, ident, seq, payload)

    sock.sendto(icmpPack, (dst, 1))
    send_time = time.time()

    recv_time, reply = recv_packet(sock)

    return  recv_time, reply, send_time

def recv_packet(sock):
    try:
        reply = sock.recv(1024)
    except socket.timeout:
        reply = "timed out"
    recv_time = time.time()

    return recv_time, reply

def checksum(source_string):
    countTo = (int(len(source_string) / 2)) * 2
    my_sum = 0
    count = 0

    while count < countTo:
        if (sys.byteorder == "big"):
            loByte = source_string[count]
            hiByte = source_string[count + 1]
        else:
            loByte = source_string[count + 1]
            hiByte = source_string[count]
        my_sum = my_sum + (ord(hiByte) * 256 + ord(loByte))
        count += 2

    if countTo < len(source_string):
        loByte = source_string[len(source_string) - 1]
        my_sum += loByte

    my_sum &= 0xffffffff

    my_sum = (my_sum >> 16) + (my_sum & 0xffff)
    my_sum += (my_sum >> 16)
    answer = ~my_sum & 0xffff
    answer = socket.htons(answer)

    return answer

try:
    dst = socket.gethostbyname(sys.argv[1])
except socket.error:
    print("Could not find host", sys.argv[1])
    quit()
sent_count = 0
success_count = 0
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

if(dst != sys.argv[1]):
    print("\nPinging " + sys.argv[1] + "[" + dst + "] with 32 bytes of data:")
else:
    print("\nPinging " + dst + " with 32 bytes of data:\n")

for c in range(0, 4):
    sock.settimeout(4.0)
    recv_time, reply, send_time = send_packet(sock, dst)
    sock.settimeout(0)
    sent_count += 1

    if (reply == "timed out"):
        print("Request timed out")
    else:
        ip = IP(reply[:20])
        icmp = ICMP(reply[20:28])
        round_time = round((recv_time - send_time)*1000)

        if(icmp.typ == 0):
            print("Reply from " + ip.src_address + " bytes=32 time=" + str(round_time) + "ms TTL=" + str(ip.ttl))
            success_count += 1
        elif(icmp.typ == 3):
            print("Reply from " + ip.src_address + ": Destination host unreachable")

    time.sleep(1)


lost_count = sent_count - success_count
print("\nPing statistics for " + dst + ":")
print("\tSent = " + str(sent_count) + ", Recieved = " + str(success_count) + ", Lost = " + str(lost_count) + " (" + str(((100/sent_count)*lost_count)) + "%)")

#functional request  and reply. format output!! DONE BANSAAII!!!
#Reply from <dst_address> bytes=32 time=<time_ms> TTL=<ttl_ip_header> DONE BANSAAAAI!!
#Set time out DONE BANSAAAI!!!!
#Checksum calculator DONE !!!
#Ping destination IP by input DONE!!!
#exception handling and cleaning
