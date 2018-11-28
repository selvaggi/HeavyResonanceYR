###################################################
# an automated code to sort and arrange authors for big Yellow report style papers
# FIRST argument points to a text file of the type <Author> {<address>} 
# e.g. Patrick Fox {Fermilab, IL} OR P~.Fox {Fermilab, IL}
# SECOND argument is where the results will be stored
#################################################### 
# Paddy Fox, 2018


#################
# function to extract author, in correct format, and institute from a big file
# returns [initials, surname, [list of institutes], [-1,-,1,..], editorFLAG] ([-1,-1,...] is a list of dummy indices to be filled later it is as long as the list of institutes)
# e.g. [P.J., Fox, Fermilab, IL, -1]
def extract_info(line):
    break_position1 = re.finditer('{', line)
    break_position2 = re.finditer('}', line)
    break_position1 = [match.start() for match in break_position1]
    break_position2 = [match.start() for match in break_position2]
#    print "working on line " + str(line)
    if (line[0] == "%") or (len(break_position1) < 1):
        return None
    institutes = [line[x+1:y] for x, y in zip(break_position1, break_position2)]
    institute_index = [-1 for i in range(len(institutes))]
#    print institutes
    author = line[:break_position1[0]]
    author = author.split()
#    print str(author)
    initials = [entry[0] for entry in author[:-1]]
    surname = author[-1]
    if initials[0][-1] != ".":
        authorinitials = initials[0] + "."
    else:
        authorinitials = initials[0]
    for initial in initials[1:]:
        if initial[-1] != ".":
            authorinitials = authorinitials + initial + "."
        else:
            authorinitials = authorinitials + initial
#    print "author = " + str(author)
#    print "institute = " + institute
    if re.search("E", line[break_position2[-1]+1:]):
#        print str(author) + " is an editor"
        editorFLAG = 1
    else:
        editorFLAG = 0
    return [authorinitials, surname, institutes, institute_index, editorFLAG]

#################
# function to scan for duplicates in list
def check_institutes(listIN, counterIN, instituteIN):
    for entry in listIN:
        indices = entry[3]
        institutes = entry[2]
        newindices = indices
        for j, institute in enumerate(institutes):
            if institute == instituteIN:
                newindices[j] = counterIN
        entry[3] = newindices
    return 0



#################
# function to put correct insitutions indices into list
def put_indices(listIN, allinstitutesIN):
    global counter
    
    for entry in listIN:
        indices = entry[3]
        institutes = entry[2]
        newindices = indices
        for j, index in enumerate(indices):
            if index > -1:
                newindices[j] = index
                continue
            else:
                newindices[j] = counter
                institute = institutes[j]
                allinstitutesIN.append([counter, institute])
                check_institutes(listIN, counter, institute)
                counter = counter + 1
        entry[3] = newindices
    return 0
            


#########################################
#########################################
#########################################
#########################################


import re, sys, shlex, subprocess
import datetime  #in python Monday =0 and Sunday =6

fileIN = open(sys.argv[1],"r")
fileOUT = open(sys.argv[2],"w")
countermin = 1
counter = countermin
allinstitutions = []

# extract info
#allinfo = [extract_info(line) for line in fileIN]
allinfo = [row for row in (extract_info(line) for line in fileIN) if row is not None]
fileIN.close()

#for row in allinfo:
#    print row

# deal with editors first
editors = [info for info in allinfo if info[-1] == 1]
N_editors = len(editors)
# sort editors on surname
editors_sorted = sorted(editors,key=lambda x: x[1])
put_indices(editors_sorted, allinstitutions)

# deal with contributors 
allcontributors = [info for info in allinfo if info[-1] != 1]
N_allcontributors = len(allcontributors)
# sort contributors on surname
allcontributors_sorted = sorted(allcontributors,key=lambda x: x[1])
#first scan over whole list for editor institutions
for entry in allinstitutions:
    check_institutes(allcontributors_sorted , entry[0], entry[1])
put_indices(allcontributors_sorted, allinstitutions)





#output authors to file 
fileOUT.write("\\author{\n") 
fileOUT.write("Editors: \\\\ \n")   
# write editor names to file   
for entry in editors_sorted:
    writeline = entry[0] + "~" + entry[1] + "$^{" + str(entry[3])[1:-1] + "}$,\,\n"
    fileOUT.write(writeline)
fileOUT.write("\\\\ \\vspace*{4mm}\n")
fileOUT.write("Contributors:\n\\\\\n")
# write contributors names to file   
for entry in allcontributors_sorted[:-1]:
    writeline = entry[0] + "~" + entry[1] + "$^{" + str(entry[3])[1:-1] + "}$,\,\n"
    fileOUT.write(writeline)
# treat last entry differently
entry = allcontributors_sorted[-1]
writeline = entry[0] + "~" + entry[1] + "$^{" + str(entry[3])[1:-1] + "}$\n\\vspace*{2.8cm}\n}\n"
fileOUT.write(writeline)
    
#output institutions to file 
fileOUT.write("\institute{\n")    
for entry in allinstitutions:
    writeline = "$^{" + str(entry[0]) + "}$ " + entry[1] + " \\\\ \n"
    fileOUT.write(writeline)
fileOUT.write("}\n\n")

    

print ("Processed " + str(N_editors) + " editors and " + str(N_allcontributors) + " authors from file " + str(sys.argv[1]))
print ("Output in file " + str(sys.argv[2]))





fileOUT.close()