import re
import glob
from nltk import *

diff_list = glob.glob("diff_*.txt")
distance_map={}
detail_map={}
pair_map = {}
for file in diff_list:
    f=open(file,"r")
    c=f.read().strip()
    diff_action = re.findall("\d[acd]\d*.*",c)
    diff_pairs = re.split("\d[acd]\d*.*\n",c)
    diff_pairs = diff_pairs[1:]

    print "file: %s" % file
    results = []
    actions = []
    action_map = {}
    action_map = {
        "a": [],
        "c": [],
        "d": []
    }
    for i, pair in enumerate(diff_pairs):
        items = pair.strip().split("---")
        action = ""
        add = re.match("\da\d",diff_action[i])
        change = re.match("\dc\d",diff_action[i])
        delete = re.match("\dd\d",diff_action[i])
    
        if change:
            action = "c"
            change1 = items[0].strip()
            change2 = items[1].strip()
            
            list1=change1[1:].split("<")
            list2=change2[1:].split(">")
            
            str1="".join(list1)
            str2="".join(list2)

        elif add:
            action = "a"
            str1 = ""
            str2 = items[0].strip()[1:]

        elif delete:
            action = "d"
            str1 = items[0].strip()[1:]
            str2 = ""

        print "str1:"
        print str1
        print "str2:"
        print str2
        print "--------------------"
        e_distance = edit_distance(str1,str2)
        actions.append(action)
        results.append(e_distance) 
        action_map[action].append(e_distance)

    distance_map[file]=(len(diff_pairs), actions, results)
    detail_map[file]=(len(diff_pairs), sum(action_map["a"]), sum(action_map["d"]), sum(action_map["c"]))

list = sorted(distance_map.items())
list2 = sorted(detail_map.items())
for i in list:
    print i[0], i[1]

for i in list2:
    print "%s\t%d\t%d\t%d\t%d" % (i[0], i[1][0], i[1][1], i[1][2], i[1][3])
