###################################################
# an automated code to remove subsubsection commands and replace with paragraph*
# takes an argument of the name of the file
# will test to see if line after \subsubsection is already \paragraph*, in which case it does nothing
#################################################### 
# Paddy Fox, 2018




#########################################
#########################################
#########################################
#########################################


import re, sys, shlex, subprocess
import datetime  #in python Monday =0 and Sunday =6

fileIN = open(sys.argv[1],"r")
fileOUT = open(sys.argv[1]+"~","w")

for counter, line in enumerate(fileIN):
#    print line
    if (line.count("\subsubsection{") == 1) or (line.count("\subsubsection*{") == 1):
        
        heading = line.split("{")
        heading = heading[1].split("}")
        heading = heading[0]
#        print "FOUND one:::::" + heading + "\n"
        nextline = next(fileIN)
        if nextline.count("\paragraph*{") != 1:
            fileOUT.write("%"+line)
            fileOUT.write("\paragraph*{"+ heading + "}\n")
            fileOUT.write(nextline)
        else:
            fileOUT.write(line)
            fileOUT.write(nextline)
    else:
        fileOUT.write(line)
        
        






fileIN.close()
fileOUT.close()

subprocess.call('rm ' + sys.argv[1], shell=True)
subprocess.call('mv ' + sys.argv[1] + "~ " + sys.argv[1], shell=True)

