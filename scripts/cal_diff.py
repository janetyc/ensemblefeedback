import os
import glob

list = glob.glob("P*_1.txt")
for file in list:
    items = file.split("_")
    pre_content = ""
    curr_content = ""
    results = []
    for i in range(1,4):
        filename1 = "%s_%s_%d.txt" % (items[0],items[1],i)
        filename2 = "%s_%s_%d.txt" % (items[0],items[1],i+1)
        os.system("diff -wB %s %s > diff_%s-%d-%d.txt" % (filename1, filename2, items[0], i, i+1))



