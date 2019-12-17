#!/usr/bin/env python3
'''
@shekharpalit
'''

'''

input to Write a contect in the cluster --> python3 blog.py alice TOC "Toc is awesome" write
input to READ a content from the cluster --> python3 blog.py chuck alice TOC "Toc is awesome" read
input to READ a content from the cluster --> python3 blog.py chuck alice TOC "Toc is awesome" take

'''
import xmlrpc.client
import sys
import proxy
naming_proxy = xmlrpc.client.ServerProxy("http://localhost:5000/", allow_none = True)

def operation():
    if len(sys.argv) <= 5:
        if sys.argv[4] == 'write':
            name = sys.argv[1]+"_ts"
            tuples = [sys.argv[1]+"_ts", sys.argv[2], sys.argv[3]]
            naming_proxy.write_to_TupleSpace(tuples)
            print("Opeartion for "+ name + " is done\n")

    elif len(sys.argv) > 5:
        if sys.argv[5] == 'read':
            name = sys.argv[1]+"_ts"
            tuples = [name, sys.argv[2]+"_ts", sys.argv[3], sys.argv[4]]
            print("values from tuplespace", naming_proxy.Read_from_TupleSpace(tuples))
            print("\n")
            print("Opeartion for " + name + " is done\n")

        elif sys.argv[5] == 'take':
            name = sys.argv[1]+"_ts"
            tuples = [name, sys.argv[2]+"_ts", sys.argv[3], sys.argv[4]]
            print("Opeartion for "+ name +  " is done\n", naming_proxy.Delete_from_TupleSpace(tuples))

        else:
            print("cannot perform operation")

if __name__ == '__main__':
    operation()
