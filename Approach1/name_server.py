import proxy
import sys

#Connecting to name_resolution adapter.
nsa = proxy.TupleSpaceAdapter('http://localhost:8004')

def name_resolution(data):

    #registered users details in file. 
    #As discussed with professor,this approach will 
    # fail since the file may be located on different server/port.
    # And file wont be accessible. So TS usage is the correct option
    file=open("log.txt","r")
    registered_users = file.read().replace('[','').replace(']','').replace("'",'').replace(' ','')
    registered_users = registered_users.split(',')
    print(registered_users,type(registered_users))
    file.close()

    #Resolve the name. Get localhost and port number of the user.
    # Replicate the data in each users TS.
    for i in registered_users:
        print(i)
        nrl = ['adapter',None]
        nrl.insert(1,i)
        #print(nrl,type(i))
        lh = nsa._rdp(nrl)
        h='"{}"'.format(lh[2])
        print("LH:",h,type(h))
        h = h.replace('"','')
        print(h)
        uts = proxy.TupleSpaceAdapter(h)
        uts._out(data)

# Recover.py calls this procedure
# Resolve the names. Get the localhost and port number of the user
# Recover data only for that user.NO REPLICATION
def recover(u,opr,tsdata):
    print("NR recieved data from RS:",u,opr,tsdata)
    nrl = ['adapter',None]
    nrl.insert(1,u)
    print("Name resolution in recovery:",nsa._rdp(nrl))
    lh = nsa._rdp(nrl)
    h='"{}"'.format(lh[2])
    #print("LH:",h,type(h))
    h = h.replace('"','')
    uts = proxy.TupleSpaceAdapter(h)
    if opr =='write':
        uts._out(tsdata)
    elif opr == 'take':
        uts._in(tsdata)
