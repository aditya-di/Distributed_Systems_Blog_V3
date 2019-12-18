import proxy

#Connect naming TS.
ts = proxy.TupleSpaceAdapter('http://localhost:8003') 
users=[["alice"],["bob"],["chuck"]]

# #Manually writing the users.
# for i in users:
#     ts._out(i)
#     print(i)


# result=ts._rdp(['alice']) 
# print(result)
 
# result=ts._inp(users)
# print(result)

# def _getuser(self,u):
#      result=ts._rdp(users)
#      print(result)


