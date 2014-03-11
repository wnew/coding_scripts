#!/usr/bin/python

#convert old type verilog module instantiations to verilog-2001 type

import sys
import re

# Load file argument contents into a single string
in_file = open(sys.argv[1])
contents = in_file.read()
in_file.close()

# Strip C-style comments, taken from http://stackoverflow.com/a/241506
def comment_remover(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return ""
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)

nocomment = comment_remover(contents)
mod_body = contents.split(";", 1)
mod_body = mod_body[1].split("\n")
new_mod_body = []

# add the new port definitions to the new module declaration
for i in mod_body:
   if not  "input" in i:
      if not "output" in i:
         if not "inout" in i:
            if not "parameter" in i:
               new_mod_body.append(i)



# Extract module declaration as section between module keyword and semicolon
mod_dec = nocomment.split('module')[1].split(';')[0]
#print mod_dec
if mod_dec.find("#") <> -1:
  print "Module declaration is already in the Verilog-2001 format"
  exit();

mod_name = mod_dec.split(" ")[1]


# get the modules ports and parameters
ports       = []
in_ports    = []
out_ports   = []
inout_ports = []
parameters  = []
contains_params = 0

def get_ports(text):
  ports = text.split(';')
  for i in ports:
     i = i.replace('\n', '').rstrip()
     i += ";"
     if "input" in i:
        in_ports.append(i.split(';')[0])
     if "output" in i:
        out_ports.append(i.split(';')[0])
     if "inout" in i:
        inout_ports.append(i.split(';')[0])
     if "parameter" in i:
        parameters.append(i.split(';')[0])

if len(parameters) != 0:
   contains_params = 1

get_ports(nocomment)

print in_ports


# build up the new module declaration
if contains_params == 1:
   new_mod_dec = "module " + mod_name + " #(\n"
   for i in parameters:
      new_mod_dec += "    " + i + ",\n"
   new_mod_dec += "  ) (\n"
else:
   new_mod_dec = "module " + mod_name + " (\n"
for i in in_ports:
  new_mod_dec += "    " + i + ",\n"
for i in out_ports:
  new_mod_dec += "    " + i + ",\n"
for i in inout_ports:
  new_mod_dec += "    " + i + ",\n"
new_mod_dec = new_mod_dec[:-2]+"\n"
new_mod_dec += ");\n"

# write the final string to the output file
out_file = open("outfile.v", 'w')
out_file.write(new_mod_dec + "\n")
for item in new_mod_body:
  out_file.write("%s\n" % item)

out_file.close()

