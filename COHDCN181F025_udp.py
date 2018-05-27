from ctypes import *
import struct
import sys
import os
import socket

class UDP(Structure):
    _fields_=[
        ("src", c_ushort),
        ("dest", c_ushort),
        ("length", c_short),
        ("checksum", c_short),
        ]

    def __new__(self, socket_buffer = None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer = None):
        self.src_port =  struct.unpack("<H", struct.pack(">H", self.src))
        self.dest_port =  struct.unpack("<H", struct.pack(">H", self.dest))

rawfile = open("udp_frame.bin", "rb").read()    #udp only stream file

udp = UDP(rawfile)
print("Source Port: " + ''.join(map(str, udp.src_port)))
print("Destination Port: " + ''.join(map(str, udp.dest_port)))
