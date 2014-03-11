#!/usr/bin/python

# strips white spaces from the end of lines
# TODO: ensure = + - * / all have spaces either side of them
# TODO: ensure , have a space after them


import sys
import re

# Load file argument contents into a single string
in_file = open(sys.argv[1])
contents = in_file.read()
in_file.close()

# open output file for writing
out_file = open(sys.argv[1] + "_clean", 'w')

# strip and write to output file
lines = contents.split("\n")
for l in lines:
   print l
   l = l.rstrip()
   print l
   out_file.write("%s\n" % l)

out_file.close()
