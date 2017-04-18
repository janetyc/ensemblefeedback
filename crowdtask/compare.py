# -*- coding: utf-8 -*-
import difflib
import re


def compareText(text1, text2):
    text1 = text1.replace("<BR>", "\n").replace(". ", ". \n").replace("! ", "! \n").replace("? ", "? \n")
    text2 = text2.replace("<BR>", "\n").replace(". ", ". \n").replace("! ", "! \n").replace("? ", "? \n")
    text1 = text1.splitlines()
    text2 = text2.splitlines()
    lineNum1 = len(text1)
    lineNum2 = len(text2)

    diff = difflib.ndiff(text1, text2)
    diff1 = []
    diff2 = []
    temp = ""

    # fix short lines
    for line in diff:
        if line.startswith("+ ") or line.startswith("- "):
            temp = line[2:]
            if temp in text1:
                diff1.append(1)
            else:
                diff2.append(1)
        elif line.startswith("  "):
            diff1.append(0)
            diff2.append(0)

    return diff1, diff2
