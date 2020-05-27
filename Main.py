import re
import os
def get_key(val,dictionary): 
    for key, value in dictionary.items():
        if val == value:
            return key 
#---------------------------------------------------
dict_noun_class={"1":"S","2":"O","3":"Ins","4":"Dat","5":"Abl","6":"Gen","7":"Loc"}
input_file=open("input.txt",encoding="utf-8")
input_lines=input_file.readlines()
output_file=open("output.txt",mode="w",encoding="utf-8")
shabdhas_regex=["S1","O2","I3","D4","A5","G6","L7"]
stop_tags=["<Numeral>","<QW>","<SPW>","<PN"+r'.*'+">"]
#---------------------------------------------------
for line in input_lines:
    print(line)
    write_line=[]#for final sentence formation
    tag_dict={}#to contain tags of each word
    tag_checklist={"<NS>":0,"<NO>":0,"<NIns>":0,"<NDat>":0,"<NAbl>":0,"<NGen>":0,"<NLoc>":0,"<V>":0}#to ensure no reptition of shabdhas and isolate adjectives
    bhav_flag=0;
    temp_f=open("bhav.txt",encoding='utf-8')
    for i in temp_f.read().split():
        if i in line:
            bhav_flag=1
     #---------------------------------------------------
    for word in line.split():
        tag_dict[word]=[]
        t_word=word.rstrip("/n")#stripping /n if any
        #---------------------------------------------------
        if(word=="|"or word=="।" or word =="।।" or word=="||" ):
            write_line.append(word)
            continue
        #---------------------------------------------------
        for i in os.listdir("Special"):#for special words
            f=open("Special\\"+i,encoding="utf-8")
            list_of_spwords=f.read().split()
            if(word in list_of_spwords):
                tag_dict[word].append("<SPW>")
            f.close()
        #---------------------------------------------------
        for i in os.listdir("Question words"):#for question words
            f=open("Question words\\"+i,encoding="utf-8")
            list_of_qwords=f.read().split()
            if(word in list_of_qwords):
                tag_dict[word].append("<QW>")
            f.close()
        #---------------------------------------------------
        for i in os.listdir("Prononun words"):#for pronouns
            f=open("Prononun words\\"+i,encoding="utf-8")
            list_of_pronouns=f.read().split()
            if(word in list_of_pronouns):
                tag_dict[word].append("<PN"+dict_noun_class[i[1]]+">")
            f.close()
        #---------------------------------------------------
        for i in os.listdir("Numeral"):#for numerals
            f=open("Numeral\\"+i,encoding="utf-8")
            list_of_numerals=f.read().split()
            if(i!="N2.txt"):#if in one to twenty
                if(word in list_of_numerals):
                    tag_dict[word].append("<Numeral>")
            else:#else check last
                for suffix in list_of_numerals:
                    temp=suffix.rstrip("/n")
                    if(re.match("^.*"+temp+"$",t_word)):
                        if(len(tag_dict[word])==0):#if the length of the tags per word is 0
                            tag_dict[word].append("<Numeral>")
            f.close()
        #---------------------------------------------------
        for i in os.listdir("Verb Regex"):# for verbs
            f=open("Verb Regex\\"+i,encoding="utf-8")
            list_of_verb_regex=f.read().split()
            for suffix in list_of_verb_regex:
                temp=suffix.rstrip("/n")
                if(i!="V2.txt"):#if present or future
                    if(re.match("^.*"+temp+"$",t_word)):
                        if(len(tag_dict[word])==0):#if the length of the tags per word is 0
                            tag_dict[word].append("<V>")
                            tag_checklist["<V>"]=1
                else:
                    if(re.match("^अ.*"+temp+"$",t_word)):#for past tense
                        if(len(tag_dict[word])==0):#if the length of the tags per word is 0
                            tag_dict[word].append("<V>")
                            tag_checklist["<V>"]=1
            
            f.close()
        
        #---------------------------------------------------
        for i in shabdhas_regex:#iterating the shabdhas types
            f=open("Shabdhas regex\\" + i +".txt",encoding="utf-8")
            shabdha_line=f.read().split()
            if('' in shabdha_line):#removal of ''
                shabdha_line.remove('')
            for suffix in shabdha_line:
                temp=suffix.rstrip("/n")
                if(re.match("^.*"+temp+"$",t_word)):#matching suffix
                    if(tag_checklist["<N"+dict_noun_class[i[1]]+">"]==0):#if the tag has not be allocated yet
                        if(len(tag_dict[word])==0) or (tag_dict[word]==["<V>"]):#if the length of the tags per word is 0
                            tag_dict[word].append("<N"+dict_noun_class[i[1]]+">")
                            tag_checklist["<N"+dict_noun_class[i[1]]+">"]=1
                        else:
                            if(tag_dict[word][0] not in stop_tags):#to ensure its not pronouns etc.,
                                try:
                                    if((int(get_key(tag_dict[word][0][2:-1],dict_noun_class))<int(i[1]))):#ensuring that lower no. type is not overwritten by above no type 
                                        tag_checklist[tag_dict[word][0]]=0#ie subject by object will not be overwritten
                                        tag_dict[word]=["<N"+dict_noun_class[i[1]]+">"]
                                        tag_checklist["<N"+dict_noun_class[i[1]]+">"]=1
                                except TypeError:
                                    continue
                            
            f.close()

        #---------------------------------------------------
        temp_string=word
        if(len(tag_dict[word])!=0):
            temp_string=temp_string+tag_dict[word][-1]
        else:
            if(bhav_flag==1):
                temp_string=temp_string+"<Adj>"
            else:
                try:
                    temp=write_line[line.split().index(word)-1]#getting previous word
                    z=re.search(r'<(.*)>',temp)#finding tag
                    temp=re.sub("<.*>","<Adj>",temp)#replacing with adj
                    write_line.pop(line.split().index(word)-1)
                    write_line.append(temp)
                    temp_string=temp_string+z.group(0)
                except IndexError:
                    temp_string=temp_string+"<Adj>"
                    
        write_line.append(temp_string)
    #---------------------------------------------------
    for i in write_line:
        output_file.write(i+" ")
    output_file.write("\n")
#---------------------------------------------------
output_file.close()
input_file.close()



