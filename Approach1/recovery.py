import json
import proxy
import os
import name_server as ns

# Log the TS events in log file
def log_ts_data(argv):
   
   # If the file is empty, it means no event has been occurred. 
    if os.stat("logs_for_recovery.txt").st_size == 0:
                    ld=str(argv).replace('(','').replace(')','')
                    file=open("logs_for_recovery.txt","a+")
                    file.write(ld+ "\n")
                    file.close()
    
    file=open("logs_for_recovery.txt","r")
    sample = file.readlines()
    print("Sample:",sample)


    with open("logs_for_recovery.txt", "r") as fd:
        for line in fd:
            line = line.strip()
            
            # (argv)!=line Event has not occurred before.
            if (str(argv)!=line):
                 ld=str(argv).replace('(','').replace(')','')
                 file=open("logs_for_recovery.txt","a+")
                 file.write(ld+ "\n")
                 file.close()
            elif (str(argv)==line): # Event occurred before, do not log the records
                print("This event has happened before/Recovery")
                break

            
            
                
        

# subscribe.py calls this method.
# When TS restarts,this block reads the data from file
def recover_ts_state():
    file=open("logs_for_recovery.txt","r")
    content = file.readlines()
    result = []
    #print("CONTENT",type(content),content)

    if os.stat("logs_for_recovery.txt").st_size <= 1:
        print("Log file is empty")
    else:
        print(os.stat("logs_for_recovery.txt").st_size)
        for line in range(len(content)):
            result.append([content[line].split("'")[1], content[line].split("'")[3],
            json.loads(content[line].split("'")[-2])])
            
            # Passing the data read from recovery_log file.
            # to the nameserver.py
        for i in result:
            u=i[0]
            opr=i[1]
            tsdata=i[2]
            ns.recover(u,opr,tsdata)








