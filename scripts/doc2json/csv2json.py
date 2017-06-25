# -*- coding: utf-8 -*-
import argparse
import csv
import json
import os

def csv2json(csvPath, csvName):
    csvFile = csvPath + "/" + csvName + ".csv"
    jsonFile = csvPath.replace("csv", "json") + "/" + csvName + ".json"

    # Parse csv file
    with open(csvFile, 'r') as infile:
        reader = csv.DictReader(infile)
        commentList = []
        for item in reader:
            commentList.append(item)
        infile.close()

    newList = covert2UIjson(commentList)
    
    # Write in json file
    with open(jsonFile, 'w+') as outfile:
        json.dump(newList, outfile, encoding="latin1")
        outfile.close()


def covert2UIjson(originalList):
    newList = []
    for item in originalList:
#        if not item: continue;
        newItem = {
            "index_start": int(item["index_start"]),
            "index_end": int(item["index_end"]),
            "mod_comment": item["comment"],
            "mod_history": item["revision_history"],
            "mod_type": item["revision_type"],
            "modifier": item["modifier"]
        }
        newList.append(newItem)

    return newList

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-C", "--csvPath", help="Input comment csv file",
                        nargs="?", default="test/csv/test.csv", type=str)
    args = parser.parse_args()

    # Parse parent directory and file name
    parentDirectory = os.path.dirname(args.csvPath)
    csvName = os.path.basename(args.csvPath).split(".")[0]

    csv2json(parentDirectory, csvName)
