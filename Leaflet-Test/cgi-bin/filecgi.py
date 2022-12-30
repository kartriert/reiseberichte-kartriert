#!/usr/bin/python3
import glob, cgi

filelist = glob.glob("./ner-results/*.geojson")
print("Content-Type: text/plain\n")
for file in filelist:
    print(file, end=";")
