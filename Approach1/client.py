import proxy
import sys
import name
import name_server as ns
import subscribe as sub

#argv[0] = Filename
#argv[1] = user alice/bob/chuck
#argv[2] = subject
#argv[3] = topic
#argv[4] = message
data = sys.argv[2],sys.argv[3],sys.argv[4]
ns.name_resolution(data)
