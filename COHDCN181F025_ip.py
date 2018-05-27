from ctypes import *
import struct
import sys
import os
import socket

class IP(Structure):
    _fields_=[
        ("version", c_ubyte, 4),
        ("ihl", c_ubyte, 4),
        ("tos", c_ubyte),
        ("length", c_ushort),
        ("ident", c_ushort),
        ("offset", c_ushort),
        ("ttl",  c_ubyte),
        ("protocol", c_ubyte),
        ("checksum", c_ushort),
        ("src", c_long),
        ("dest", c_long)
        ]

    def __new__(self, socket_buffer = None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer = None):
        self.src_address = socket.inet_ntoa(struct.pack("@I", self.src))
        self.dest_address = socket.inet_ntoa(struct.pack("@I", self.dest))
        self.id = struct.unpack("<H", struct.pack(">H", self.ident))

proto = {1:"ICMP", 2:"IGMP", 6:"TCP"}

rawfile = open("google.bin", "rb").read()   #ip only stream file

ip = IP(rawfile)

print("Source IP: " + str(ip.src_address))
print("Destination IP : " + str(ip.dest_address))
print("Protocol : " + proto[ip.protocol])
print("ID : " + ''.join(map(str, ip.id)))
