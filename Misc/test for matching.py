import re
dict_noun_class={"1":"S","2":"O","3":"Ins","4":"Dat","5":"Abl","6":"Gen","7":"Loc"}
f=open("Shabdhas regex\M1.txt",encoding="utf-8")
l=f.readlines()
x=input("Enter:")
tag=""
for i in l:
    for j in i.split():
        z=j.rstrip("/n")
        if(re.match("^.*"+z+"$",x)):
            print(x,z)
            
        
