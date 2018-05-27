from ctypes import *
import struct
import sys
import os
import socket

class TCP(Structure):
    _fields_=[
        ("src", c_ushort),
        ("dest", c_ushort),
        ("seq_no", c_long),
        ("ack_no", c_long),
        ("offset", c_ubyte, 4),
        ("reserved", c_ubyte, 4),
        ("flag",  c_ubyte),
        ("window", c_ushort),
        ("checksum", c_ushort),
        ("urg_point", c_ushort),
        ]

    def __new__(self, socket_buffer = None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer = None):
        self.src_port =  struct.unpack("<H", struct.pack(">H", self.src))
        self.dest_port =  struct.unpack("<H", struct.pack(">H", self.dest))

proto = {1:"ICMP", 2:"IGMP", 6:"TCP"}

rawfile = open("tcp_frame.bin", "rb").read()    #tcp only stream raw file

tcp = TCP(rawfile)
print("Source Port: " + ''.join(map(str, tcp.src_port)))
print("Destination Port: " + ''.join(map(str, tcp.dest_port)))
