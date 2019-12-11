#!/usr/bin/env python3
'''
@shekharpalit
'''

import sys
import struct
import socket
from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread
import concurrent.futures
import proxy
import datetime
import json
import time

naming_proxy = proxy.TupleSpaceAdapter('http://localhost:8004')


MAX_UDP_PAYLOAD = 65507

server = SimpleXMLRPCServer(("localhost", 5000), allow_none = True)
map_tuple_uri = {}
ack_track = {}

def replicate_tuple_to_all(name, data):
    global map_tuple_uri, ack_track
    for key, val in map_tuple_uri.items():
        if key != name:
            replicate_proxy = proxy.TupleSpaceAdapter(val[0])
            replicate_proxy._out(data)

    return "Sucessfully replicated\n"

def delete_from_file(data):
    with open("log_data.txt","r+") as f:
        new_f = f.readlines()
        f.seek(0)
        str_data = str(data[:len(data)-1])[1:-1]
        str_data.split(",")
        str_data = "[" + str_data + ","
        str_data.replace("None,", "")
        for line in new_f:
            if str_data not in line:
                f.write(line)
        f.truncate()
    return True

def delete_from_all(name, data):
    global map_tuple_uri
    for key, val in map_tuple_uri.items():
        if key != name:
            delete_proxy = proxy.TupleSpaceAdapter(val[0])
            delete_proxy._in(data)
    if delete_from_file(data):
        return True

def logging(data):
    with open('log_data.txt', 'a') as f:
        f.write(str(data))
        f.write("\n")
    return True

def write_to_TupleSpace(data_from_RPC):
    global map_tuple_uri, ack_track
    if map_tuple_uri[data_from_RPC[0]][1] == True:
        URI = map_tuple_uri[data_from_RPC[0]][0]
        operation_on_Ts = proxy.TupleSpaceAdapter(URI)
        ts = datetime.datetime.now().timestamp()
        data_from_RPC.append(str(ts))
        operation_on_Ts._out(data_from_RPC)
        t3 = Thread(target=replicate_tuple_to_all, args=(data_from_RPC[0], data_from_RPC))
        t3.start()
        t3.join(2)
        if ack_track[data_from_RPC[-1]] >= 2:
            if logging(data_from_RPC):
                del ack_track[data_from_RPC[-1]]

def Read_from_TupleSpace(data_from_RPC):
    global map_tuple_uri
    if map_tuple_uri[data_from_RPC[0]][1] == True:
        URI = map_tuple_uri[data_from_RPC[0]][0]
        operation_on_Ts = proxy.TupleSpaceAdapter(URI)
        res = operation_on_Ts._rd([data_from_RPC[1],data_from_RPC[2], data_from_RPC[3], None])
    return str(res)

def Delete_from_TupleSpace(data_from_RPC):
    global map_tuple_uri
    if map_tuple_uri[data_from_RPC[0]][1] == True:
        URI = map_tuple_uri[data_from_RPC[0]][0]
        operation_on_Ts = proxy.TupleSpaceAdapter(URI)
        res = operation_on_Ts._in([data_from_RPC[1],data_from_RPC[2], data_from_RPC[3], None])
        if delete_from_all(data_from_RPC[0], [data_from_RPC[1],data_from_RPC[2], data_from_RPC[3], None]):
            return str(res)


def async_check_helper(URI):
    check_stats = proxy.TupleSpaceAdapter(URI)
    try:
        active_node = check_stats._rd([None, None, None, None])
        print(active_node)
        if active_node:
            return True
    except Exception as e:
        print("Node is not active")
        return False


def check_status_for_nodes():
    global map_tuple_uri
    for key, val in map_tuple_uri.items():
        with concurrent.futures.ThreadPoolExecutor() as executor:
            print("inside check")
            results = [executor.submit(async_check_helper, val[0])]
            for f in concurrent.futures.as_completed(results):
                print(f.result())
                if f.result():
                    map_tuple_uri[key][1] = True
                    print(map_tuple_uri)
                else:
                    map_tuple_uri[key][1] = False
                    print(map_tuple_uri)


def recover_TupleSpace(URI):
    file = open("log_data.txt","r")
    content = file.readlines()
    results = []
    if content ==['\n']:
        print("Log file is empty")
    else:
        for line in range(len(content)):
            results.append([content[line].split("'")[1], content[line].split("'")[3],content[line].split("'")[5],
            json.loads(content[line].split("'")[-2])])
    for result in results:
        URI._out(result)
    file.close()

def main(address = '224.0.0.1', port = '54322'):
    server_address = ('', int(port))
    global map_tuple_uri, ack_track
    size = 100
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    group = socket.inet_aton(address)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Listening on udp://{address}:{port}")

    try:
        while True:
            data, _ = sock.recvfrom(MAX_UDP_PAYLOAD)
            notification = data.decode()
            namecheck = None

            notifications_string = notification.split(' ')
            notifications_string_tuple = ' '.join(notifications_string[2:])[1:-1]
            notifications_string_tuple_value = notifications_string_tuple.split(',')
            res = []
            for char in notifications_string_tuple_value:
              res.append(char[1:-1])
            if notifications_string[1] == 'adapter':
                get_URI_proxy =  proxy.TupleSpaceAdapter(str(notifications_string[2]))
                if notifications_string[0] not in map_tuple_uri:
                    map_tuple_uri[notifications_string[0]] = [notifications_string[2], True]
                recover_TupleSpace(get_URI_proxy)

            elif notifications_string[1] == 'write':
                ack_track[res[-1]] = 1
                ack_track[res[-1]] += 1

            # check_status_for_nodes()
    except Exception as e:
        print(e)
        sock.close()


def usage(program):
    print(f'Usage: {program} ADDRESS PORT', file=sys.stderr)
    sys.exit(1)

def server_handler_for_write():
    server.register_function(write_to_TupleSpace, 'write_to_TupleSpace')
    server.serve_forever()

def server_handler_for_delete():
    server.register_function(Delete_from_TupleSpace, 'Delete_from_TupleSpace')
    server.serve_forever()

def server_handler_for_read():
    server.register_function(Read_from_TupleSpace, 'Read_from_TupleSpace')
    server.serve_forever()

t0 = Thread(target=server_handler_for_write)
t0.start()

t1 = Thread(target=server_handler_for_read)
t1.start()

t2 = Thread(target=server_handler_for_delete)
t2.start()

def heartbeat():
    while True:
        time.sleep(30)
        check_status_for_nodes()


if __name__ == '__main__':
    t = Thread(target=heartbeat)
    t.start()
    main()
