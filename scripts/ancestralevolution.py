# -*- coding: utf-8 -*-
"""

Combined molecular and structural evolution

"""

# Imports
import pandas as pd
import numpy as np
import os
import json
import argparse
from Bio import SeqIO
#import altair as alt
#!pip install ete3
#from ete3 import Tree
#from tqdm import tqdm

BASEDIR = os.getcwd()
print("We are operating out of base directory:", BASEDIR)

parser = argparse.ArgumentParser()
parser.add_argument('--slac_json', default='', help='Input SLAC JSON file location', required=True)
parser.add_argument('--output_dna', default='', help='Output Codon/DNA FASTA file location', required=True)
parser.add_argument('--output_aa', default='', help='Output Amino-Acid FASTA file location', required=True)
parser.add_argument('--output_msa', default='', help='Output Multiple sequence alignment FASTA file location', required=True)

args = parser.parse_args()

SLAC_JSON = os.path.join(BASEDIR, args.slac_json)
print("# Reading SLAC JSON File:", SLAC_JSON)

def get_JSONData(json_file):
    with open(json_file, "r") as fh:
        json_data = json.load(fh)
    return json_data
#end method

def get_Codon(sequence, codon_site):
  return data["branch attributes"]["0"][sequence]["codon"][0][codon_site]
#end method

def get_NodePairs(t):
  pairs = {}
  for node in t.traverse("preorder"):
    #print([node.name], node.children)
    if len(node.children) > 0 and node.name != '':
      pairs[node.name] = {}
      #print(node.children[0].name)
      children = []
      for child in node.children:
        children.append(child.name)
      #end for
      pairs[node.name] = children
  #end for
  return pairs
#end method

data          = get_JSONData(SLAC_JSON)
tree          = data["input"]["trees"]["0"] + ";"
num_sequences = data["input"]["number of sequences"]
num_sites     = data["input"]["number of sites"]
#t             = Tree(tree, format=1)
#pairs         = get_NodePairs(t) # returns a dictionary
#node_order    = [node.name for node in t.traverse("preorder")]

# Get SLAC Sequences
data_dict = {}
data_dict_DNA = {}
data_dict_AA = {}

for species in data["branch attributes"]["0"].keys():
  #print(species)
  #data_dict[species] = {"DNA": "".join(data["branch attributes"]["0"][species]["codon"][0]),
  #                      "AA": "".join(data["branch attributes"]["0"][species]["amino-acid"][0])}
  print("# Adding:", species)
  data_dict_DNA[species] = "".join(data["branch attributes"]["0"][species]["codon"][0])
  data_dict_AA[species] = "".join(data["branch attributes"]["0"][species]["amino-acid"][0])
#end for

print("Completed loading")

# Output DNA Fasta file and AA file
with open(args.output_dna, 'w') as handle:
    #    SeqIO.write(data_dict_DNA.values(), handle, 'fasta')
    for k in data_dict_DNA:
        #print(">" + k + "\n" + str(data_dict_DNA[k]) + "\n", file=handle)
        #print(">" + str(k) + "\n" + "\n", file=handle)
        #print()
        print("# Writing:", k)
        sp = k 
        molecule = data_dict_DNA[k].replace("---", "")
        print(">" + k + "\n" + molecule, file=handle)
    #end for
#end with

with open(args.output_aa, 'w') as handle:
    for k in data_dict_AA:   
        print("# Writing:", k)
        molecule = data_dict_AA[k].replace("-", "")
        print(">" + k + "\n" + molecule, file=handle)
    #end for
#end with

with open(args.output_msa, 'w') as handle:
    for k in data_dict_DNA:
        print("# Writing:", k)
        sp = k
        #molecule = data_dict_DNA[k].replace("---", "")
        molecule = data_dict_DNA[k]
        print(">" + k + "\n" + molecule, file=handle)
