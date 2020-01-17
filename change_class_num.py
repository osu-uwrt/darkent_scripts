#!/usr/bin/env python3

import glob

replacements = {
    "10": "0"
}

annotationFiles = glob.glob("data/**/*.txt", recursive=True)
for annotationFile in annotationFiles:
    lines = []
    for line in open(annotationFile, "r"):
        splitLine = line.split(" ")
        if splitLine[0] in replacements:
            splitLine[0] = replacements[splitLine[0]]
        lines.append(" ".join(splitLine))
    with open(annotationFile, "w") as f:
        f.writelines(lines)
