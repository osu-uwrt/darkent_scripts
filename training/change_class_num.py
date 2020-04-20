#!/usr/bin/env python3

import glob

print("Replacing class numbers...")
# Which class numbers should be replaced with what
replacements = {
    "10": "0",
    "6": "0"
}

# For each annotation...
annotationFiles = glob.glob("data/**/*.txt", recursive=True)
for annotationFile in annotationFiles:
    lines = []
    # Read each line and replace the class number if it should be
    for line in open(annotationFile, "r"):
        splitLine = line.split(" ")
        if splitLine[0] in replacements:
            splitLine[0] = replacements[splitLine[0]]
        lines.append(" ".join(splitLine))
    with open(annotationFile, "w") as f:
        f.writelines(lines)

print("Done")