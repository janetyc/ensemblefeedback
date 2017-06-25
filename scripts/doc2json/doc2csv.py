# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

import argparse
import csv
import json
import os
import sys
import zipfile


def parse_revision(soupDoc, soupCom):
    index = 0
    elementID = -1
    commentID = -1
    currentElement = {"index_start": index + 1, "index_end": index + 1,
                      "modifier": "", "revision_type": "",
                      "revision_history": "", "comment": ""}
    commentElement = {"index_start": index + 1, "index_end": index + 1,
                      "modifier": "", "revision_type": "",
                      "revision_history": "", "comment": ""}
    feedbackList = []

    # Parse revision to dictionary
    for paragraph in soupDoc.body:
        for element in paragraph:
            if element.name == "commentRangeStart":
                commentID = element["w:id"]
                print "comment start"
                print commentID

                if currentElement:
                    if currentElement["index_end"] != index:
                        commentElement = {"index_start": index + 1,
                                          "index_end": index + 1,
                                          "modifier": "",
                                          "revision_type": "Comment",
                                          "revision_history": "",
                                          "comment": ""}
                        for text in soupCom.find(attrs={"w:id": str(element["w:id"])}).find_all("t"):
                            commentElement["comment"] += text.string + "\n\n"
                    else:
                        commentElement = None
                        for text in soupCom.find(attrs={"w:id": str(element["w:id"])}).find_all("t"):
                            currentElement["comment"] += text.string + "\n\n"
                        if currentElement["revision_type"] == "":
                            currentElement["revision_type"] = "Comment"


            elif element.name == "commentRangeEnd":

                if element["w:id"] == commentID:
                    if commentElement:
                        commentElement["index_end"] = index
                        feedbackList.append(commentElement)
                    else:
                        currentElement["index_end"] = index
                print "comment end :%s" % commentID
                print currentElement


            re_history_str = element.find("t").string if element.find("t") else "None"
            if element.name == "ins":
                if (elementID != element["w:id"] and
                        ["index_end"] != index):
                    elementID = element["w:id"]
                    if currentElement:
                        feedbackList.append(currentElement)

                    currentElement = {"index_start": index + 1,
                                      "index_end": index + 1,
                                      "modifier": "",
                                      "revision_type": "Insert",
                                      "revision_history":
                                      "\"" + re_history_str + "\"",
                                      "comment": ""}
                else:
                    if currentElement["revision_type"] != "Comment":
                        currentElement["revision_type"] = "Replace"
                        prefix = currentElement["revision_history"]
                        currentElement["revision_history"] = prefix + " with \"" + \
                            re_history_str + "\""
                    else:
                        currentElement["revision_type"] = "Insert"
                        currentElement["revision_history"] = "\"" + \
                            re_history_str + "\""

                comment = element.find("commentRangeStart")
                if comment:
                    for text in soupCom.find(attrs={"w:id": str(comment["w:id"])}).find_all("t"):
                        currentElement["comment"] += text.string + "\n"

            elif element.name == "del":
                del_txt = "".join([i.text for i in element.find_all("delText")])
                if elementID != element["w:id"]:
                    elementID = element["w:id"]
                    if currentElement:
                        feedbackList.append(currentElement)

                    currentElement = {"index_start": index + 1,
                                      "index_end": index + 1,
                                      "modifier": "",
                                      "revision_type": "Delete",
                                      "revision_history":
                                      #"\"" + element.find("delText").string + "\"",
                                      "\"" + del_txt + "\"",
                                      "comment": ""}
                else:
                    if currentElement["revision_type"] != "Comment":
                        currentElement["revision_type"] = "Replace"
                        suffix = currentElement["revision_history"]
                        currentElement["revision_history"] = "\"" + \
                            element.find("delText").string + "\" with " + suffix
                    else:
                        currentElement["revision_type"] = "Delete"
                        currentElement["revision_history"] = "\"" + \
                            re_history_str + "\""

                comment = element.find("commentRangeStart")
                if comment:
                    for text in soupCom.find(attrs={"w:id": str(comment["w:id"])}).find_all("t"):
                        currentElement["comment"] += text.string + "\n"
                
                index += len(del_txt)
                currentElement["index_end"] = index
            else:
                for text in element.find_all("t"):
                    index += len(text.string)

            

    return feedbackList


def doc2csv(docPath, docName):
    xmlPath = docPath.replace("doc", "xml")
    xmlDocument = xmlPath + "/" + docName + "_document.xml"
    xmlComments = xmlPath + "/" + docName + "_comments.xml"

    # Read in xml file from test/xml
    with open(xmlDocument) as infile:
        soupDoc = BeautifulSoup(infile.read(), 'xml')
        infile.close()
    with open(xmlComments) as infile:
        soupCom = BeautifulSoup(infile.read(), 'xml')
        infile.close()

    # Parse revision from xml file
    feedbackList = parse_revision(soupDoc, soupCom)
    feedbackList = [item for item in feedbackList if item["revision_type"] != ""]
    feedbackList.sort(key=lambda x: (x['index_start'], x['index_end']), reverse=False)
    return feedbackList

def originaldoc2txt(docPath, docName):
    xmlPath = docPath.replace("doc", "original_xml")
    xmlDocument = xmlPath + "/" + docName + "_document.xml"

    # Read in xml file from test/xml
    with open(xmlDocument) as infile:
        soupDoc = BeautifulSoup(infile.read(), 'xml')
        infile.close()

    context_ori = ""
    for a in soupDoc.body.find_all("p"): # Each paragraph
        for b in a.find_all("r"):
            for c in b.find_all("t"):
                context_ori += c.string
        context_ori += "\n"


    txtPath = docPath.replace("doc", "txt")
    txtFile = txtPath + "/" + docName + ".txt"
    with open(txtFile, 'w') as f:
        f.write(context_ori.encode("utf-8"))
        f.close()

def list2csv(docPath, docName, feedbackList):
    csvPath = docPath.replace("doc", "csv")
    csvFile = csvPath + "/" + docName + ".csv"
    with open(csvFile, "w+") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["index_start", "index_end", "modifier", "revision_type",
                         "revision_history", "comment", "form"])
        for item in feedbackList:
            row = []
            row.append(item["index_start"])
            row.append(item["index_end"])
            row.append(item["modifier"])
            row.append(item["revision_type"])
            row.append(item["revision_history"])
            row.append(item["comment"])
            row.append("")
            writer.writerow([unicode(s).encode("utf-8") for s in row])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-D", "--docPath", help="Input original docx file",
                        nargs="?", default="test/doc/test.docx", type=str)
    # parser.add_argument("-C", "--csvPath", help="Output feedback csv file",
    #                     nargs="?", default="test/csv/test.csv", type=str)
    args = parser.parse_args()

    # Parse parent directory and file name
    parentDirectory = os.path.dirname(args.docPath)
    docName = os.path.basename(args.docPath).split(".")[0]

    # Get result list from docx
    feedbackList = doc2csv(parentDirectory, docName)
    # Write list to csv file
    list2csv(parentDirectory, docName, feedbackList)

    print "save original txt"
    originaldoc2txt(parentDirectory, docName.strip("-revised")) #save to txt file
