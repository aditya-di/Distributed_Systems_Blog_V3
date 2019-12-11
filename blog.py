#!/usr/bin/env python3
'''
@shekharpalit
'''

import xmlrpc.client
import sys
import proxy
naming_proxy = xmlrpc.client.ServerProxy("http://localhost:5000/", allow_none = True)

def opeartion():
    if sys.argv[4] == 'read':
        name = sys.argv[1]+"_ts"
        tuples = [name, sys.argv[2]+"_ts", sys.argv[3], sys.argv[4]]
        print("values from tuplespace", naming_proxy.Read_from_TupleSpace(tuples))
        print("\n")
        print("Opeartion for" + name + "is done\n")

    if sys.argv[4] == 'write':
        name = sys.argv[1]+"_ts"
        tuples = [sys.argv[1]+"_ts", sys.argv[2], sys.argv[3]]
        naming_proxy.write_to_TupleSpace(tuples)
        print("Opeartion for"+ name + "is done\n")

    if sys.argv[4] == 'take':
        name = sys.argv[1]+"_ts"
        tuples = [name, sys.argv[2]+"_ts", sys.argv[3], sys.argv[4]]
        print("Opeartion for"+ name +  "is done\n", naming_proxy.Delete_from_TupleSpace(tuples))




# def operations_for_Alice():
#     name = sys.argv[1]+"_ts"
#     alice_tuples = [sys.argv[1]+"_ts", sys.argv[2], sys.argv[3]]
#     naming_proxy.write_to_TupleSpace(alice_tuples)
#     print("Opeartion for Alice is done\n")
#
#
# def opearations_for_Bob():
#     # name = sys.argv[1]+"_ts"
#     # name_resolved = naming_proxy.getURI(name)
#     # blog = proxy.TupleSpaceAdapter(name_resolved)
#     # bob_tuples = [sys.argv[1]+"_ts", sys.argv[2], sys.argv[3]]
#     # blog._out(bob_tuples)
#     # print("Opeartion for Bob is done\n")
#     # name = sys.argv[1]+"_ts"
#     name = sys.argv[1]+"_ts"
#     bob_tuples = [name, sys.argv[2]+"_ts", sys.argv[3], sys.argv[4]]
#     # print(chuck_tuples)
#     # naming_proxy.Delete_from_TupleSpace(bob_tuples)
#     print("Opeartion for bob is done\n", naming_proxy.Delete_from_TupleSpace(bob_tuples))
#
# def operations_for_chuck():
#     name = sys.argv[1]+"_ts"
#     chuck_tuples = [name, sys.argv[2]+"_ts", sys.argv[3], sys.argv[4]]
#     # print(chuck_tuples)
#     print("values from tuplespace", naming_proxy.Read_from_TupleSpace(chuck_tuples))
#     print("\n")
#     print("Opeartion for Chuck is done\n")

if __name__ == '__main__':
    operation()
