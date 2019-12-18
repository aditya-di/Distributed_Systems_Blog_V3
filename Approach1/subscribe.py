#!/usr/bin/env python3

import sys
import struct
import socket
import proxy
import recovery as r
ulist=[]
# per <https://en.wikipedia.org/wiki/User_Datagram_Protocol>
MAX_UDP_PAYLOAD = 65507


def main(address='224.0.0.1', port = '54321'):
    # See <https://pymotw.com/3/socket/multicast.html> for details

    server_address = ('', int(port))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)

    group = socket.inet_aton(address)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    na = proxy.TupleSpaceAdapter('http://localhost:8003')
    nsa = proxy.TupleSpaceAdapter('http://localhost:8004')

    print(f"Listening on udp://{address}:{port}")
    #print("in main")


    try:
        while True:
            data, _ = sock.recvfrom(MAX_UDP_PAYLOAD)
            notification = data.decode()
            print(notification)
            l=notification.split(' ')
            print("Notification:",notification)
            if l[1] =='start': #When TS starts,register the user in file
                global ulist
                if(l[0] in ulist) == False:
                    ulist.append(l[0])

                log_users()
                r.recover_ts_state()

            elif l[1] == 'adapter':
                nsl = []
                nsl.append(l[1])
                nsl.append(l[0])
                nsl.append(l[2])
                nsa._out(nsl)
            elif l[0].lower() =='alice' or l[0].lower() == 'bob' or l[0].lower() == 'chuck' :
                print("Log data in recovery file:",l)
                r.log_ts_data(l)




    except:
        sock.close()


def usage(program):
    print(f'Usage: {program} ADDRESS PORT', file=sys.stderr)

    sys.exit(1)

def log_users():
    global ulist
    file=open("log.txt","w")
    file.write(repr(ulist))
    file.close()


if __name__ == '__main__':
    # if len(sys.argv) != 3:
    #     usage(sys.argv[0])
    main()



    #sys.exit(main(*sys.argv[1:]),0)
