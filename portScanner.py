#!/usr/bin/python

import socket
import sys
import ping
import telnetlib
import tempfile

FILE = tempfile.NamedTemporaryFile(delete=False, dir='/tmp')

print("Log file {}".format(FILE.name))
if 4!=len(sys.argv):
    FILE.write("Please enter {} <IP> <start port> <end port>".format(sys.argv[0]) +'\n')
    print("Please enter {} <IP> <start port> <end port>".format(sys.argv[0]))
    exit()
    
start_port = 0
end_port = 0

try:
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])
    percent, lost, maximum = ping.quiet_ping(sys.argv[1])
except:
    FILE.write("check port numbers,execute the script as root" +'\n')
    print("check port numbers,execute the script as root")    
    exit()

if (start_port > end_port or start_port == 0 or end_port == 0 or 
    start_port > 65535 or end_port > 65535):
    print("Error: Start port should be lower or eaqual end port, "
          "ports can`t be 0 or bigger than 65535")
    exit()

if percent == 100:
    FILE.write("IP {} is unreachable".format(sys.argv[1]) +'\n')
    print ("IP {} is unreachable".format(sys.argv[1]))
    exit()
     
while start_port <= end_port:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((sys.argv[1],start_port))
        sock.close()
        FILE.write("Port {} is opened".format(start_port) +'\n')
        print("Port {} is opened".format(start_port))
        tn = telnetlib.Telnet(sys.argv[1],start_port)
        tn.write('\n')
        outpt = tn.read_until("Password:",10)
        tn.close()
        FILE.write("Output data: \n {}".format(outpt) +'\n')
        print("Output data: \n {}".format(outpt))
        start_port = start_port + 1
        
    except:
        print("Port {} is closed".format(start_port))
        start_port = start_port + 1

FILE.close()







