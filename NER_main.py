
import json, requests, ast ,re
from sentimentanalysis import  cleaner, sentiment
import sentimentanalysis.FullNNP as fullname
from collections import Counter
from city_name_dict import *
from location_dictionary import *
from and_condition import *
import urllib
import urllib2
import time as tag 
import time as extract 
import sys
from stanford import client101
from nltk.stem.wordnet import WordNetLemmatizer

#coding: utf8 
import os
import unicodedata
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('utf-8')
nnp_list_list = []
a = []
done = []
location_list = []
name_list = []
output_location = []
output_lastname = []
remaining = []
list_dictionary = []
tree1 = []

import nltk
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk import stem
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk import stem

sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')



def split_into_sentences(text):
    pattern = "\.[A-Z]"
    # print text
    regex = re.findall(pattern, text, flags=0)
    regex = list(set(regex))
    if regex:
        for ele in regex:
            text = text.replace(ele,'. ' + ele[-1])
    # print text
    sents = sent_tokenizer.tokenize(text)
    return sents

def extract_curr(text):
    c101 = '(\-?\$\d{1,9}\.*\d+\s(billion|Billion|million|Million|trillion|Trillion|pounds))'
    c201 = '(\-?\d{1,9}\.*\d*\s(billion|Billion|million|Million|trillion|Trillion)+\s(pounds))'

    c102 = '\-?\$\d{1,4}'
    c104 = '((Rs)\s*\d+\,*\d*\s*(crore|lakh|thousand|rupees|Crore|Lakh|Thousand|Rupees)*)'
    c105 = '(\-?\$\d+\s(billion|Billion|million|Million|trillion|Trillion|dollars|pounds)*)'
    c119 = '(\-?\d+\.*\d*\s(billion|Billion|million|Million|trillion|Trillion|dollars|pounds))'
    # c106 = '((Rs)\s*\d+)'
    res = []
    # f1 = open 
    bigger = False

    flag = 0


    if bigger == False:
        cm105 = re.findall(c105, text)
        for x in cm105:
            # print "105" 
            res.append(x[0])
            # bigger = True

        

        # if bigger == False:
        #     cm102 = re.findall(c102, text)
        #     for x in cm102:
        #         print "102" 
        #         res.append(x)
        #         # bigger = True


    if bigger == False:
        cm104 = re.findall(c104, text)
        for x in cm104:
            # print "104"
            res.append(x[0])
            bigger = True

        # if bigger == False:
        #     cm106 = re.findall(c106, text)
        #     for x in cm106:
        #         print "106"
        #         res.append(x[0])
        #         bigger = True

        # bigger = False 

    if bigger == False:
        cm201 = re.findall(c201, text)
        for x in cm201:
            # print "/201"
            res.append(x[0])

        if bigger == False:
            cm101 = re.findall(c101, text)
            for x in cm101:
                # print "101" 
                flag = 1
                res.append(x[0])
                # bigger = True

            if bigger == False:
                cm119 = re.findall(c119, text)
                for x in cm119:
                    # print "119" , flag 
                    if flag != 1:
                        res.append(x[0])
                    bigger = True


    

    # if bigger == False:
    #     cm103 = re.findall(c103, text)
    #     for x in cm103:
    #         print "103"
    #         # print '..', x[0]
    #         res.append(x[0])
    #         bigger = True

    return list(set(res))

def extract(text):

    # text = text.lower() 
    text = text.replace(',' ,"")
    exp = "(next|last|coming|upcoming|past)"
    durs = "(years|days|week|months|quarters|quarter|month|year|day|minutes|minute|seeconds|second)"
    r8 = exp + "\s(\d*)\s" + durs # Next 120 days
    suff = "s"
    month = '(january |february |march |april |may |june |july |august |september |october |november |december |jan |feb |mar |apr|may |jun |jul |aug |sep |sept |oct |nov |dec |January | February |March | April |May |June |July |August |September |October |November |December |Jan |Feb |Mar |Apr |May |Jun |Jul |Aug |Sep |Sept |Oct |Nov |Dec )'
    terms = '(tomorrow|today|yesterday|tonight|fiscal year|afternoon|noon|evening|morning|night|dawn|dusk)'  
    days = '(monday|tuesday|wednesday|thursday|friday|saturday|sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)'
    year = "((18|19|20)\d{2}\s*)" 
    date_no = "\d{0,2}(th|st|nd|rd|,)?"

    # r103= "\d{0,2}(th)?\s("+month+")\s((18|19|20)\d{2})" ## 20th Jan 2012 and similar
    # r3 = "(" + monthx + ")\s" + date_no ## Jan 10
    # r4 =  date_no + "\s(" + monthx + ")" ## 10 Jan
    r5 =  year 
    # r6 = "(" + monthx + ")" 
    # r7 = r6 + "\s" + r5
    r61 = month
    r88 = '(\d{4}'+suff+')'
    
    r107 = '(\d+[t|s|n][h|t|d]\s*'+month + ')'
    r101 = '\d{2}[-]\d{2}[-]\d{2,4}'
    r102 = '\d\d\s[A-Za-z][A-Za-z][A-Za-z]\s\d\d\d\d'
    r103 = '(((\d{0,1,2,3,4,5}[t|s|n][h|t|d]\s*'+month+'\s*\,*\s*\d+)))'
    # r111 = '((18|19|20)\d{2})'
    r104 = '(' + month + '\s* \d+[t|s|n][h|t|d]\,*\s*\,*\d+ )' 
    r106 = '(' + month + '\s* \d+[t|s|n][h|t|d]\s*)'
    r117 = '(' +month + '\s*\d{1,2})'
    r118 = '(' + month + '\s)'
    r11 = terms 

    r108 = '(\d\d\s*' + durs + ')'
    r109 = '(((1?[0-9]|2[0-3]):[0-5][0-9])\s*[a|p|P|A][m|M])'
    r333 = days
    res = []
    
    bigger = False

    if bigger == False:
        m333 = re.findall(r333, text)
        for x in m333:
            # print "333" , x
            res.append(x)
            bigger = True  


    if bigger == False:
        m117 = re.findall(r117, text)
        for x in m117:
            # print "117" 
            res.append(x[0])
            bigger = True

    if bigger == False:
        m5 = re.findall(r5, text)
        for x in m5:
            # print "/5" 
            res.append(x[0])
            bigger = True  

    if bigger == False:
        m103 = re.findall(r103, text)
        for x in m103:
            # print "103"
            res.append(x[0])
            bigger = True
        if bigger == False:
            m107 = re.findall(r107, text)
            for x in m107:
                # print "107"
                res.append(x[0])
                # bigger = True'''
        bigger = False 

    
    # if bigger == False:
    #         m111 = re.findall(r111, text)
    #         for x in m111:
    #             print "111" 
    #             res.append(x[0])
    #             # bigger = True
    if bigger == False:
            m109 = re.findall(r109, text)
            for x in m109:
                # print "109" 
                res.append(x[0])
                # bigger = True
    
    if bigger == False:
            m11 = re.findall(r11, text)
            for x in m11:
                # print "11" 
                res.append(x)
                # bigger = True

    if bigger == False:
            m101 = re.findall(r101, text)
            for x in m101:
                # print /"101" 
                res.append(x)
                # bigger = True
    if bigger == False:
        m88 = re.findall(r88 , text)
        for x in m88:
            # print "88"
            res.append(x)
            # bigger = True



    if bigger == False:
        m104 = re.findall(r104, text)
        for x in m104:
            # print "104"
            res.append(x[0])
            bigger = True

        if bigger == False:
            m106 = re.findall(r106, text)
            for x in m106:
                # print "106"
                res.append(x[0])
                bigger = True

        bigger = False


    if bigger == False:
        m102 = re.findall(r102, text)
        for x in m102:
            # print "102"
            res.append(x)
            # print x
            bigger = True
    
    if bigger == False:
        m108 = re.findall(r108, text)
        for x in m108:
            # print "108" 
            res.append(x[0])
            # bigger = True

    if bigger == False:
        m118 = re.findall(r118, text)
        for x in m118:
            # print "118"
            res.append(x[0])
            # bigger = True

    if bigger == False:
        m61 = re.findall(r61, text)
        for x in m61:
            # print "118"
            res.append(x.strip())
            # bigger = True

    
    return list(set(res))

def number_presence(val):
    m = re.search('\d+', val)
    
    if m:
        return 1

def find_word_in_sent(sent, alist):
    sent = sent.lower()
    sent = sent.split(' ')
    result = []
    for ele in alist:
        if ele in sent:
            ind = sent.index(ele)
            string = ''
            if number_presence(sent[ind-1]) == 1:
                string = string +' ' + sent[ind-1]

            string = string +' ' + sent[ind]

            if number_presence(sent[ind+1]) == 1:
                string = string+ ' ' + sent[ind+1]
            string = string.strip()
            # print string
            result.append(string)

    return result


#Navigation dictionaries to find child dictionary of our NNP in question
def recursive_dict(dictum, nnp):
    # print dictum
    dictret = []
    if type(dictum) == dict:
        # print dictum 
        if dictum['node'].find(nnp)>0:
            dictret.append(dictum['node'])
            if len(recursive_dict(dictum['subTree'],nnp))>0:
                dictret.append(recursive_dict(dictum['subTree'],nnp))       
        else:
            if len(recursive_dict(dictum['subTree'],nnp))>0:
                dictret.append(recursive_dict(dictum['subTree'],nnp))
    else:
        for dictrow in dictum:
            if dictrow['node'].find(nnp)>0:
                dictret.append(dictrow['node'])
                if len(recursive_dict(dictrow['subTree'],nnp))>0:
                    dictret.append(recursive_dict(dictrow['subTree'],nnp))
                              
            else:
                if len(recursive_dict(dictrow['subTree'],nnp))>0:
                    dictret.append(recursive_dict(dictrow['subTree'],nnp))

    return dictret


def getData1(text, delimiter, bd, sentiment):
    url = 'http://localhost:8080/sae-1.0.0-BUILD-SNAPSHOT/analytics/analyse'
    json_data = {"sentence":text, "bd":bd, "sentiment":sentiment, "delimiter":delimiter}
    headers = {"Content-type": "application/json","Accept": "application/json"}
    jsonData = json.dumps(json_data)
    response = requests.post(url, headers=headers, data=jsonData)
    return response.json()




def make_tree(line):
    bd = getData1(line, bd=True, sentiment=False, delimiter="-")
    bd = "["+str(bd)+"]"
    bd = ast.literal_eval(bd)
    return bd


def breakmultilist(l):
    outlist = []
    if len(l) == 0:
        outlist = l
    elif len(l)==1 and type(l[0]) == list:
        outlist = breakmultilist(l[0])
    elif len(l)>1 and type(l[0]) == list:
        outl = []
        for each in l:
            outl.append(breakmultilist(each))
        outlist = outl
    else:
        outlist = l
    return outlist

def cleannode(x):
    x = x[x.find('->')+2:]
    # x = x.split('(')[0]
    return x

def clean_actor(acters):
    actor_list=[]
    for actor in acters:
        # print actor
        if type(actor)!=list:
            actor=cleannode(actor).strip()
            actor_list.append(actor)
        else:
            actor=breakmultilist(actor)
            actor_list.extend(clean_actor(actor))
    return actor_list

####All NNP and NNS
def all_nnps(tree):
    all_nnp=[]
    keyword_pos=['NNP' ]
    for key in keyword_pos:
        actor_list=breakmultilist(recursive_dict(tree[0],key))
        clean_name=clean_actor(actor_list)
        if clean_name not in all_nnp:
            all_nnp.append(clean_name)

    return all_nnp


def combine ( list1 , rel ):
    ans = []
    for i in list1:
        ans.append(i)

    ans.append(rel)

    return ans 

def combine1 ( list1 , short):
    ans = []
    for i in list1:
        for j in i :
            ans.append(j)

    ans.append(short)

    return ans

# def fun_NNP (tree, origtree ,a , ans_list):
#     for subTree_dic in tree :
#         orig_node = subTree_dic['node']
#         if get_pos_rel(orig_node)['word'] == a:
#             # print a
#             inside_trees = subTree_dic['subTree']
#             if  get_pos_rel(get_node_parent(orig_node, inside_trees, origtree))['pos'] != "NNP":
#                 node = get_node_parent(orig_node, inside_trees, origtree)
#                 print node , "node"
#                 print tree[0] , "tree"
#                 full = fullname.fullnnp(origtree[0] , node.strip().strip("->").strip()) 
#                 print type(full) , full , "????????????????/"
#                 ans_list.append(full[0][0]) 
           
#         else :
#             inside_trees = subTree_dic['subTree']
#             fun_NNP (inside_trees, origtree,a,ans_list)

def fun_NNP1 (tree, origtree ,a , ans_list):
    for subTree_dic in tree :
        orig_node = subTree_dic['node']
        if get_pos_rel(orig_node)['word'] == a:
            inside_trees = subTree_dic['subTree']
            # print a, get_node_parent(orig_node, inside_trees, origtree)
            if  get_pos_rel(get_node_parent(orig_node, inside_trees, origtree))['pos'] != "NNP":
                # print '...',orig_node
                # print origtree
                nnode = sentiment.filter_node(orig_node)
                # print '*(*',nnode
                node = get_next_parallel_nodes(nnode, tree)[1]
                # print node

                if len (node) == 0:
                    s = ""
                    s+= nnode
                    t = []
                    t.append(s)
                    tt = []
                    tt.append(get_pos_rel(nnode)['pos'])
                    ans_list.append(t)
                    ans_list.append(tt)
                    ans_list.append(get_pos_rel(nnode)['rel'])
                    ans_list.append(get_pos_rel(nnode)['word'])
                else :
                    for each in node:

                        if each['pos'] == 'NNP':
                            # print a ,"AAAAAAAAAA"
                            # print each, "nodeeeeeeeeeeeeeeeeeeeeeeeeee"

                            s = ""
                            s+= a +" "+each['word']
                            t = []
                            t.append(s)
                            tt = []
                            tt.append(each['pos'])
                            ans_list.append(t)
                            ans_list.append(tt)
                            ans_list.append(each['rel'])
                            ans_list.append(each['word'])
                        # print ans_list , "OOOOOOOOOOOOOOOOOOOOOOOOOO"
                # print tree[0] , "tree"
                # full = fullname.fullnnp(origtree[0] , node.strip().strip("->").strip()) 
                # print type(full) , full , "????????????????/"
                # ans_list.append(full[0][0]) 
           
        else :
            inside_trees = subTree_dic['subTree']
            fun_NNP1 (inside_trees, origtree,a,ans_list)


#####Build Dictionary for every sentence and its corresponding Noun Phrase , POS , relation#########
def build_dictionary(fo):
    ans = {}
    q = []
    global tree1 
    for i,each in enumerate(fo) :
        cc = []
        tree = make_tree(each)
        tree1 = tree
    
        # sentiment.tree_parse(tree[0])  #To print the tree
        
        list1 = all_nnps(tree)
        # print list1 , "??"
        for ac in list1 :
            for li in ac:
                # print "li" ,li 
                if ( li != "") :
                    s = re.findall ('(nn)', li )
                    if ( len(s) == 0):
                        bb = []
                        # print '***',li
                        relation  = li.split('(', 1)[1].split(')')[0]
                        # print li , relation , ">>>>>>>"
                        short = li.split('-')[0]
                        # print short , "::::" 

                        ll = (fullname.fullnnp(tree[0],li))
                        # print ll , "ll"
                        if relation == "nsubj" or relation == "conj" or relation == "pobj" or relation == "dobj":
                            bb.append(combine ( ll , relation))
                            # print bb , "bb"
                            cc = combine1( bb , short)
                            # print cc , "cc"
                            q.append(cc)
                            # print q , "QQQ"
                    else :
                        # print '**99*',li
                        if get_pos_rel(li)['pos'] == "NNP":
                            a = get_pos_rel(li)['word']
                            # print a
                            ans_list = []
                            # fun_NNP (tree[0] ,tree[0] , a , ans_list)
                            fun_NNP1 (tree[0] ,tree[0] , a , ans_list)

                            # print ans_list , "::::"
                            if len (ans_list) > 0 :
                                q.append(ans_list)
                                # print q , "MMMMMMMM"
                            # print recursive_dict(tree[0] , "NNP") , "?:?????:?::"
                            # print get_node_parent(li, tree[0] ,tree[0] )

        ans[each] = q


    # print ans , "LLLL"
    return ans 




#######Inserting the elements in the dictionary in proper format#####
def insert_dictionary (final_dic , dic, fo) :
    for index , each in enumerate(fo):
        final_dic[index] = {}
        if (len(dic[each])) > 0:
            for i,j in enumerate(dic[each]):
                final_dic[index][i] = {}
                final_dic[index][i]['NounPhrase'] = dic[each][i][0][0].encode('utf-8')
                final_dic[index][i]['POS'] = dic[each][i][1][0].encode('utf-8')
                final_dic[index][i]['Relation'] = dic[each][i][2].encode('utf-8')
                final_dic[index][i]['Root'] = dic[each][i][3].encode('utf-8')
                # print final_dic[index]


    # print final_dic , "?????"

    return final_dic


#####Print the dictionary in proper format##########
def print_dictionary(final_dic , nnp_list_list):
    # print final_dic , "????????????"
    for i , u in enumerate(final_dic):
        # print "Sentence Number :" , i
        nnp_list=[]
        for j,v in enumerate(final_dic[i]):
            nnp_info={}
            nnp_info['NounPhrase']=final_dic[i][j]['NounPhrase']
            nnp_info['POS']=final_dic[i][j]['POS']
            nnp_info['Relation']=final_dic[i][j]['Relation']
            nnp_info['Root'] = final_dic[i][j]['Root']
            nnp_list.append(nnp_info)

        nnp_list_list.append(nnp_list)

    # print "Nounphrase list" ,nnp_list_list
    return nnp_list_list

def location(address,key):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
    api_key = str(key)
    fullurl = url + address + '&key=' + api_key
    r = requests.get(fullurl)

    data = json.loads(r.text)
    
    if len(data['results'])!=0:
        add = data['results'][0]['address_components']
        res1 = {}
        res1['status']=data['status']
        return res1 , add 
    else:
        add = 'NULL'
        res1={}
        res1['status']=data['status']
        return res1 , add


def find_location(list_dictionary,done):
    a = []
    
    for i,each in enumerate(list_dictionary):
        for j in range(len(list_dictionary[i])):
            ff = list_dictionary[i][j]['NounPhrase']

            if ff not in done:
	            if ( len(ff.split()) > 0):
	                # if ff not in done :
	                #     try :
	                #         ff = City_name_changes[ff]
	                #     except:
	                #         ff = ff
	                    
	                #     try :

	                #         if ( dic_location[ff]  == 1):
	                #             a.append(ff)
	                    
	                #     except :
	                    ###Output Files Address
	                        APi_Result=open('OutputV07.txt','w')
	                        ###########Key files
	                        key_detail_list=open('Api_Keys.txt','r').read().split('\n')
	                        key_id=0
	                        key=str(key_detail_list[key_id])
	                        

	                        result=[]
	                        keyList=[]
	                        res =location(ff.encode('utf-8'),key)
	                        # if ff == 'm':
	                        # print res   #To check the geo api result
	                        if res[0]['status'] == 'OK':
	                            for ii in range(len(res[1])): 
	                                if res[1][ii][ u'long_name']== ff or res[1][ii][u'short_name'] == ff :
	                                    flag = 0
	                                    for j in range(len(res[1][ii][u'types'])):

                                            
	                                        if res[1][ii][u'types'][j] == u'sublocality_level_1':
	                                            flag = 1
                                        
	                                        elif res[1][ii][u'types'][j] == u'sublocality':
	                                            flag = 1
	                                        elif res[1][ii][u'types'][j] == u'political':
	                                            flag = 1
                                            
	                                        elif res[1][ii][u'types'][j] == u'continent':
	                                            flag = 1

	                                    if (flag == 1):
	                                        # print "Location:" ,ff 
	                                        dic_location[ff] = 1;
	                                        fout = open('location_dictionary.py', 'w')
	                                        fout.write('dic_location = '+str(dic_location))
	                                        a.append(ff)

	                        elif res[0]['status']=='OVER_QUERY_LIMIT':
	                            key_id+=1
	                            key=str(key_detail_list[key_id])
	                            # print key
	                            res=location(ff.encode('utf-8'),key)

    

    return a



def  NER_company(input_sen,done,list_dictionary):

    suffix_dic = {}

    company = []
    bad_char = open('bad chars.txt' ,'r').read().strip().split('\n')
    bad_char = [x.replace('\r','') for x in bad_char]
    suffix = open('suffix.txt' ,'r').read().split('\n')
    office = open ('CompanyNameFinal.txt' , 'r').read().strip().split('\n')

    office_dic = {}
    for each in office:
        each1 = each.lower().strip()
        office_dic[each1] = 1;


    for each in suffix :
        each1 = each.lower()
        each2 = each1.strip()
        
        suffix_dic[each2] = 1;
  

    for i,each in enumerate(list_dictionary[0]):
        token =  (list_dictionary[0][i]['NounPhrase'])
        # print token , "PPP "
        if token not in done :
            token1 = token.lower().strip()
            # lmtzr = WordNetLemmatizer()
            # token2 = lmtzr.lemmatize(token1 , 'v')
            # print token , token2 , "??"
            if token1 in office_dic:
                if office_dic[token1] == 1:
                    # print token1 , "1"
                    company.append(token)

    for i,each in enumerate(list_dictionary[0]):
        token =  (list_dictionary[0][i]['NounPhrase'])

        if token not in done :
            token1 = token.lower()
            
            for each in bad_char:
                token1 = token1.replace(each," ")

            split_token = token1.split(" ")
            temp = []
            length = len(split_token)
            for each in reversed(split_token):
                temp.append(each)
                temp2 = reversed(temp)
                ss = ""
                for each in temp2:
                    ss = ss+" "+each
                ss = ss.strip()
                if ss in suffix_dic:
                    if ( suffix_dic[ss] == 1 and length != 1):
                        company.append(token) 
                        break

            
    output1 = list(set(company))
    # print output1 , "LL"
    return  output1

def NER_currency(input_sen,done):
    ########Finding Currency##########
    curr_list = []
    a = extract_curr(input_sen)
    if (len(a)>0) and a not in done:
        curr_list.append(a)

    # print "Currency :" ,curr_list
    temp = []
    for i in range(len(curr_list)):
        for j,each in enumerate(curr_list[i]):
            temp.append(each)

    return temp


def NER_date(input_sen,done):
    ########Finding Date###########
    date_list = []
    
    a = extract (input_sen)

    if (len(a) >0) and a not in done:
        date_list.append(a)

    

    temp = []
    for i in range(len(date_list)):
        for j,each in enumerate(date_list[i]):
            temp.append(each)
        
    return temp

def NER_location (input_sen,done,list_dictionary):
    return list(set(find_location (list_dictionary,done)))


def NER_lastname(input_sen, done,list_dictionary):

    last_name = open('NameListfinal.txt' ,'r').read().split('\n')
    output = []
    last_name_dic = {}
    for each in last_name:
        each1 = each.lower().strip()
        last_name_dic[each1]= 1; 

    for i,each in enumerate(list_dictionary[0]):
        token =  (list_dictionary[0][i]['NounPhrase'])
        flag= 0
        for s in token.split():
            if (s.isdigit()):
                flag =1
                break

        if flag == 0 :
            if token not in done and list_dictionary[0][i]['POS']!= "NN":
                token1 = token.lower()
                # print token1

                split_token = token1.split(" ")
                temp = []
                length = len(split_token)
                if length > 0 :
                    if split_token[length-1] in last_name_dic:
                        if last_name_dic[split_token[length-1]]== 1:
                            output.append(token)

    output1 = list(set(output))
    return  output1 

def merge ( done , output):
    for each in output:
        done.append(each.strip())

    return done

# def first_cap(alist):
#     if alist[0].isupper() :
#         return True
#     else:
#         return False  

# def fun_prep(tree, origtree ,a, list_dictionary):
#     for subTree_dic in tree :
#         inside_trees = subTree_dic['subTree']
#         orig_node = subTree_dic['node']
#         # print orig_node
#         if get_pos_rel(orig_node)['pos'] == "NNP" :
#             # print get_pos_rel(orig_node)['word'] , "??"
#             if get_pos_rel(orig_node)['rel'] == 'nsubj' or get_pos_rel(orig_node)['rel'] == 'dobj' or get_pos_rel(orig_node)['rel'] == 'pobj':
#                 s = ""
#                 if  len(subTree_dic['subTree']) > 0 :
#                 # s = ""
#                     s+= cleannode(subTree_dic['subTree'][0][u'node']).lstrip().rsplit('-')[0]
#                     s+= " "
#                 s+= get_pos_rel(orig_node)['word']
#                 name_list.append(str(s))
#                 # print name_list
#         node = get_pos_rel(orig_node)['word']
#         # print node 
#         # 

#         if get_pos_rel(orig_node)['rel'] == 'pobj':
#             inside_trees = subTree_dic['subTree']
#             if get_pos_rel(get_node_parent(orig_node, inside_trees, origtree))['rel'] == 'prep':
#                 if get_pos_rel(get_node_parent(orig_node , inside_trees, origtree))['word'] == 'to' :
#                     # print get_pos_rel(orig_node) , list_dictionary
#                     # print get_pos_rel(orig_node)['word'] , list_dictionary[0][1]['NounPhrase']
#                     for k,each in enumerate(list_dictionary[0]):
#                         if get_pos_rel(orig_node)['word'] in list_dictionary[0][k]['NounPhrase']:
#                             if first_cap (list_dictionary[0][k]['NounPhrase']):
#                                 location_list.append(list_dictionary[0][k]['NounPhrase'])


#         if node.lower().strip() ==  'said' or node.lower().strip() ==  'says': 
#             for subTree_dic2 in inside_trees:
#                 orig_node2 = subTree_dic2['node']
#                 node2 = get_pos_rel(orig_node2)['word']
#                 # print node2
#                 if get_pos_rel(orig_node2)['pos'] == 'NNP':
#                     if node2 in list_dictionary[0][0]['NounPhrase']:
#                         name_list.append(list_dictionary[0][0]['NounPhrase'])
              
            
        
#         fun_prep (inside_trees, origtree,a,list_dictionary)


def fullNER ( text_list , done , list_dictionary):

    result = {}

    output_date = NER_date(text_list,done )
    done = merge (done , output_date)
    result["Date"] = output_date

    output_curr = NER_currency(text_list,done)
    done = merge (done , output_curr)
    result ["Money"] = output_curr

    output_location =  NER_location(text_list,done,list_dictionary)
    # print output_location
    # output_location1 =  first_cap(output_location)
    done = merge (done , output_location)

    result["Location"] = output_location

    output_lastname  = NER_lastname(text_list,done,list_dictionary)
    done = merge (done , output_lastname)
    result["Person"] = output_lastname

    output_company = NER_company(text_list,done , list_dictionary)
    done = merge (done , output_company)
    result["organisation"] = output_company

    
    
    # print result , "____________"
    return result

def antilog(x):
    return 10 ** x

def gp ( length):
    if length > 1:
        r = antilog(float(1)/float(length-1))
    else :
        r = 10
    a = 1

    gp_series = []

    if length == 1:
        gp_series.append( pow ( r, 1))
    else :
        for i in range(length):
            gp_series.append( pow ( r , i))

    # print gp_series , "GGGGGGGGG"
    return  gp_series


def pdf_name ( remaining):
    prob_name = {}
    last_name = open('NameListfinal.txt' ,'r').read().split('\n')
    last_name_dic = {}
    for each in last_name:
        each1 = each.lower().strip()
        last_name_dic[each1]= 1;  

    length = len (remaining.split())
    gp_series = gp (length)
    p = 0
    for i , element in enumerate (remaining.split()):
        element1 = element.lower().strip()
        
        if last_name_dic.has_key(element1):
            if last_name_dic[element1] ==  1:
                p += gp_series[i]


    return p



def pdf_organisation ( remaining):
    prob_organsation = {}
    unique_company_dic = {}
    unique_company = open('CompanyNameFinal.txt' ,'r').read().split('\n')
    for each in unique_company:
        each1 = each.lower().strip()
        unique_company_dic[each1]= 1; 

    length = len (remaining.split())
    gp_series = gp (length)
    p = 0
    for i , element in enumerate (remaining.split()):
        element1 = element.lower().strip()
        if element1 in unique_company_dic :
            if unique_company_dic[element1] == 1:
                p += gp_series[i]
                # print gp_series[i] , element , "_____"

    return p

###########Main Function####################

def final_NER ( text , nnp_list_list):
    text_list=[]
    text_list.append(text)
    final_dic = {}
    r4 = []
    r5 = []
    dic = build_dictionary(text_list) 
    dic1 = insert_dictionary(final_dic, dic, text_list)
    list_dictionary = print_dictionary(dic1,nnp_list_list)

    tree = make_tree(text)

    r1 = fullNER ( text , done ,list_dictionary)


    for i,each in enumerate(list_dictionary[0]):
        token =  (list_dictionary[0][i]['NounPhrase'])
        if token not in done:
            remaining.append(token)

    # for each in remaining:
    #     for every in each.split():
    for each in remaining:
        score_organsation =  pdf_organisation(each.replace('.',' '))
        score_name = pdf_name(each.replace('.',' '))

        # print each , "Organization" , score_organsation
        # print each , "Person" , score_name

        if score_organsation- score_name >= 8:
            r4.append(each)
            remaining.remove(each)
        elif score_name - score_organsation >= 8:
            r5.append(each)
            remaining.remove(each)

    if len(r4) > 0 :
    	for each in r4:
    		r1["organisation"].append(each)
    if len(r5) >0 :
    	for each in r5:
    		r1["Person"].append(each)

    # fun_prep(tree[0], tree[0] ,a , list_dictionary)

    # print "Remaining" , remaining
    # r3 =  (r1["Location"])
    # for each in location_list:
    #     if each  in remaining:
    #         r3.append(each)
    #         remaining.remove(each)
    # r1["Location"] = r3


    r2 =  (r1["Person"])
    for each in name_list:
        if each in remaining:
            # print each 
            r2.append(str(each))

    r1["Person"] = r2    
    return  r1 

def notinAshu ( Phrase , Ashu_NER):
    # print Phrase , Ashu_NER ,"::::::::::::::;"
    for each in (Ashu_NER):
        if len(Ashu_NER[each]) > 0:
            if Phrase in Ashu_NER[each]:
                return False
        
    return True
# print tree1 , "QQQQQQQ"





def func(tree , origtree , word , bool1):
    res = []
    for subTree_dic in tree :
        # print "!!!" , subTree_dic
        inside_trees = subTree_dic['subTree']
        # print "!!!" , inside_trees
        orig_node = subTree_dic['node']
        # print get_pos_rel(orig_node)['word'] , word 
        if get_pos_rel(orig_node)['word'] == word:
            # print get_pos_rel(orig_node)['word'] , "??"
            if get_pos_rel(get_node_parent(orig_node, inside_trees, origtree))['word'] == 'at' or get_pos_rel(get_node_parent(orig_node, inside_trees, origtree))['word'] == 'to' or get_pos_rel(get_node_parent(orig_node, inside_trees, origtree))['word'] == 'in':
                # print get_pos_rel(get_node_parent(orig_node, inside_trees, origtree))
                res.append(True)
                # print bool1 
        # if res != True:
        res.extend(func(inside_trees , origtree , word , bool1))

    return res


def rule1_at_to(remaining):
    global tree1
    # print  "??" , tree1
    org = [] 
    for each in remaining:
        root = ""
        bool1 = False
        for np in nnp_list_list[0]:
            # print np , "LL"
            if each == np['NounPhrase']:
                if len (func( tree1[0] , tree1[0] , np['Root'] , bool1)) > 0 :
                    if func( tree1[0] , tree1[0] , np['Root'] , bool1)[0] == True:
                        # print np['NounPhrase'] + " is a organisation"
                        remaining.remove( np['NounPhrase'])
                        org.append(np['NounPhrase'].strip())
                        return org
                    else:
                        continue

    return org  


def Innovaccer_NER( statement):
    Stanford_last = {}
    Ashu_NER = {}

    statement1 = statement.replace( '$' ,' $ ').replace(',' ,' , ')
    tree = make_tree(statement)

    Ashu_NER = final_NER(statement, nnp_list_list)
    # print "Ashutosh NER" , Ashu_NER 
    Stanford_dic = {}

    # print remaining , "OOOOOOOOOOOOOOOOOOOOOOOOOO"

    if len (remaining) > 0 :
        Stanford_dic =  client101.Stanford_NER (statement1)
        print "STanford NER " , Stanford_dic
    c = 0


    
    money = []
    organisation= []
    person = []
    location = []
    date = []
   

    at_to_org_list = []
    at_to_org_list = rule1_at_to (remaining) # Rule to identify 'at' 
    if len(at_to_org_list) > 0 :
        for each in at_to_org_list:
            Ashu_NER['organisation'].append(each) # Adding the organisations 


    for each in remaining:
        for every in each.split():
            if every  in Stanford_dic:
                if Stanford_dic [every] == "PERSON":
                    p = ""
                    for every1 in each.split():
                        if every1 in Stanford_dic:
                            if Stanford_dic[every1] == "PERSON":
                                p+= every1
                                p+=" "

                    p.strip()
                    
                    if p not in Ashu_NER['Person']:
                        Ashu_NER['Person'].append(p.strip())
                        break

                elif Stanford_dic [every]  == "LOCATION":
                    l = ""
                    for every1 in each.split():
                        if every1 in Stanford_dic:
                            if Stanford_dic[every1] == "LOCATION":
                                l+= every1
                                l+=" "

                    l.strip()
                    if l not in Ashu_NER['Location']:
                        Ashu_NER['Location'].append(l.strip())
                        break
                elif Stanford_dic [every]  == "ORGANIZATION":
                    o = ""
                    for every1 in each.split():
                        if every1 in Stanford_dic:
                            if Stanford_dic[every1] == "ORGANIZATION":
                                o+= every1
                                o+=" "

                    o = o.strip()
                    # print o , Ashu_NER['organisation'] , "::::"
                    if o not in Ashu_NER['organisation']:
                        Ashu_NER['organisation'].append(o.strip())
                        
                    flag = 0 ;
                    for i , each in enumerate(Ashu_NER['organisation']):
                        for k in each.split():
                            if k.strip() == o.strip() :
                                flag = 1;

                    if flag == 0 :
                        Ashu_NER['organisation'].append(o.strip())

                    Ashu_NER['organisation'] = list(set(Ashu_NER['organisation']))
                    # print Ashu_NER['organisation'] , "QQQQQQQ"


                # elif Stanford_dic [every]  == "DATE":
                #     d = ""
                #     for every1 in each.split():
                #         if every1 in Stanford_dic:
                #             if Stanford_dic[every1] == "DATE":
                #                 d+= every
                #                 d+=" "

                #     d.strip()
                #     if d not in Ashu_NER['Date']:
                #         Ashu_NER['Date'].append(d)


                elif Stanford_dic [every]  == "MONEY":
                    m = ""
                    for every1 in each.split():
                        if every1 in Stanford_dic:
                            if Stanford_dic[every1] == "MONEY":
                                m+= every
                                m+=" "

                    m.strip()
                    flag = 0;
                    # print Ashu_NER['Money']
                    for i , each in enumerate(Ashu_NER['Money']):
                        for k in each.split():
                            if k.strip() == m.strip() :
                                flag = 1;

                    if flag == 0 :
                        Ashu_NER['Money'].append(m.strip())
                        break

    # print Ashu_NER , ")))))))))))))))))))))))))))"


    for each in Stanford_dic:
        # print each , remaining
        if each in remaining:
            if Stanford_dic[each] == 'ORGANIZATION':
                flag = 0

                for company in Ashu_NER['organisation']:
                    if each.strip() in company.split():
                        flag = 1
                        break 

                if flag == 0:
                	Ashu_NER['organisation'].append(each.strip())
                	


            if Stanford_dic[each] == 'LOCATION':
                flag = 0
                for place in Ashu_NER['Location']:
                    if each.strip() in place.split():
                        flag = 1
                        break 

                if flag == 0:
                	Ashu_NER['Location'].append(each.strip())
                	
            if Stanford_dic[each] == 'PERSON':
                flag = 0
                for name in Ashu_NER['Person']:
                    if each.strip() in name.split():
                        flag = 1
                        break    

                if flag == 0:
                	Ashu_NER['Person'].append(each.strip())
                	
    return Ashu_NER

'''
      # print Ashu_NER , ")))))))))))))))))))))))))))"
    # print Stanford_dic , "PPPPPPPPPPPPPPPPP"
    # for i,each in enumerate(statement1.split()):
    #     # print i , each 
    #     if each in Stanford_dic:
    #         # print each 
    #         if len(Stanford_dic[each]) > 0:
    #             if Stanford_dic[each] == "MONEY":
    #                 # print  index ,i , "???"
    #                 if i-index_m == 1 or i == 0:
    #                     money.append(each)
    #                     index_m = i
    #                 else :
    #                     # print index , i , ">>>>>"
    #                     if len(money) != 0:
    #                         money.append('|')
    #                     money.append(each)
    #                     index_m = i
    #             elif Stanford_dic[each] == "DATE":
    #                 # print Stanford_dic[each] , "PPP"
    #                 if i-index_d == 1 or i == 0:
    #                     # print each , "::"
    #                     date.append(each)
    #                     index_d = i
    #                 else :
    #                     # print index , i , ">>>>>"
    #                     if len(date) != 0:
    #                         date.append('|')
    #                     date.append(each)
    #                     index_d = i
    #             elif Stanford_dic[each] == "ORGANIZATION":
    #                 if i-index_o == 1 or i == 0:
    #                     organisation.append(each.strip())
    #                     index_o = i
    #                 else :
    #                     # print index_o , i , ">>>>>"
    #                     if len(organisation) != 0:
    #                         organisation.append('|')
    #                     organisation.append(each.strip())
    #                     index_o = i
    #             elif Stanford_dic[each] == "PERSON":
    #                 if i-index_p == 1 or i == 0:
    #                     person.append(each.strip())
    #                     index_p = i
    #                 else :
    #                     # print index_o , i , ">>>>>"
    #                     if len(person) != 0:
    #                         person.append('|')
    #                     person.append(each.strip())
    #                     index_p = i
    #             elif Stanford_dic[each] == "LOCATION":
    #                 # print Stanford_dic[each] , "PPP"
    #                 if i-index_l == 1 or i == 0:
    #                     # print each , "::"
    #                     location.append(each.strip())
    #                     index_l = i
    #                 else :
    #                     # print index , i , ">>>>>"
    #                     if len(location) != 0:
    #                         location.append('|')
    #                     location.append(each.strip())
    #                     index_l = i
    # org1 = []
    # money1 = []
    # date1 = []
    # person1 = []
    # location1 = []
    # for i , each in enumerate (money) :
    #     if i == 0:
    #         # money1 = []
    #         s = ""
    #     if each != "|":
    #         s += each
    #         s+= " "

    #     if each == "|" or i == len(money)-1:
    #         money1.append(s.strip())
    #         s = ""

    # for i , each in enumerate(date) :
    #     if i == 0:
    #         # date1 = []
    #         s = ""
    #     if each != "|":
    #         s += each
    #         s += " "

    #     if each == "|" or i == len(date)-1:
    #         date1.append(s.strip())
    #         s = ""

    # for i , each in enumerate (organisation) :
    #     if i == 0:
    #         # org1 = []
    #         s = ""
    #     if each != "|":
    #         s += each
    #         s += " "

    #     if each == "|" or i == len(organisation)-1:
    #         org1.append(s.strip())
    #         s = ""

    # for i , each in enumerate (person) :
    #     if i == 0:
    #         # org1 = []
    #         s = ""
    #     if each != "|":
    #         s += each
    #         s += " "

    #     if each == "|" or i == len(person)-1:
    #         person1.append(s.strip())
    #         s = ""

    # for i , each in enumerate (location) :
    #     if i == 0:
    #         # org1 = []
    #         s = ""
    #     if each != "|":
    #         s += each
    #         s += " "

    #     if each == "|" or i == len(location)-1:
    #         location1.append(s.strip())
    #         s = ""

    # Stanford_last["MONEY"] = list(set(money1))
    # Stanford_last["DATE"] = list(set(date1))
    # Stanford_last["ORGANISATION"] = list(set(org1))
    # Stanford_last["PERSON"] = list(set(person1))
    # Stanford_last["LOCATION"] = list(set(location1))
    # print "STanford " , Stanford_last 

   
    # # # full_NER = {}


    # for each in nnp_list_list : 
    #     for i in each :
    #         if notinAshu ( i['NounPhrase'] , Ashu_NER):
    #             Phrase1 =  i['NounPhrase']
    #             # print Phrase1 , ""
    #             for each in Stanford_last:
    #                 if Phrase1 in Stanford_last[each]:
    #                     if each == "DATE":
    #                         Ashu_NER["Date"].append(Phrase1) 
    #                     if each == "MONEY":
    #                         Ashu_NER["Money"].append(Phrase1) 
    #                     if each == "ORGANISATION":
    #                         Ashu_NER["organisation"].append(Phrase1) 
    #                     if each == "LOCATION":
    #                         Ashu_NER["Location"].append(Phrase1) 
    #                     if each == "PERSON":
    #                         Ashu_NER["Person"].append(Phrase1) 

    # for each in Stanford_last:
    #     if each == "DATE":
    #         for every in Stanford_last[each]:
    #             if notinAshu ( every , Ashu_NER):
    #                 for i, element in enumerate(nnp_list_list[0]):
    #                     if every in nnp_list_list[0][i]['NounPhrase']:
    #                         Ashu_NER['Date'].append(every)

    #     if each == "MONEY":
    #         for every in Stanford_last[each]:
    #             if notinAshu ( every , Ashu_NER):
    #                 for i,element in enumerate(nnp_list_list[0]):
    #                     if every in nnp_list_list[0][i]['NounPhrase']:
    #                         Ashu_NER['Money'].append(every)

    #     if each == "ORGANISATION":
    #         for every in Stanford_last[each]:
    #             if notinAshu ( every , Ashu_NER):
    #                 for i , element in enumerate(nnp_list_list[0]):
    #                     if every in nnp_list_list[0][i]['NounPhrase']:
    #                         Ashu_NER['organisation'].append(every)

    #     if each == "LOCATION":
    #         for every in Stanford_last[each]:
    #             if notinAshu ( every , Ashu_NER):
    #                 for i , element in enumerate(nnp_list_list[0]):
    #                     if every in nnp_list_list[0][i]['NounPhrase']:
    #                         Ashu_NER['Location'].append(every)

    #     if each == "PERSON":
    #         for every in Stanford_last[each]:
    #             if notinAshu ( every , Ashu_NER):
    #                 for i , element in enumerate(nnp_list_list[0]):
    #                     if every in nnp_list_list[0][i]['NounPhrase']:
    #                         Ashu_NER['Person'].append(every)

'''

  

if __name__=="__main__":


	statement = open('newyork.txt' ,'r').read().split('\n')
	for each in statement:
		print Innovaccer_NER (each)
