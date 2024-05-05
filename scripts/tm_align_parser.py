# Imports
import re
import os
import sys
import pandas as pd
from tqdm import tqdm
import glob

# Declares
#data_files = [sys.argv[1]]

data_files = glob.glob(os.path.join("..",
                                    "results",
                                    "TMAlignResults",
                                    "*.txt"))

print("# We will process:", len(data_files), "files")

output_csv = os.path.join ("..",
                           "tables",
                           "TM_Align_Results.csv")

file = open(output_csv, "w", newline="")

file.truncate(0) # Clears file

#sys.exit(1)

data_dict = {"Name of Chain_1:": "",
             "Name of Chain_2:": "",
             "Length of Chain_1:": "",
             "Length of Chain_2:": "",
             "Aligned length=": "",
             "RMSD=": "",
             "Seq_ID=n_identical/n_aligned=": "",
             "TM-score=": "", # Done 3 times
             "Normalized_Chain_1_TM_Score": "",
             "Normalized_Chain_2_TM_Score": "",
             "Normalized_Average_TM_Score": "",
}

count = 1

# --- Helper functions ---
def process(line, _dict):
    for item in _dict.keys():
        if item in line:
            split_key = item[-1]
            # Aligned length=  284, RMSD=   3.57, Seq_ID=n_identical/n_aligned= 0.810
            #if item == "Aligned length=":
            #    data = line.split(",")[0]
            #    print(data)
            #elif
            #end if
            
            #Length of Chain_1:  341 residues
            #Length of Chain_2:  341 residues
            if item == "Length of Chain_1:" or item == "Length of Chain_2:":
                current_line = line.replace("residues", "")
                data = current_line.split(split_key)
                _dict[item] = data[1].strip()
            elif item == "Aligned length=":
                # Aligned length=  284, RMSD=   3.57, Seq_ID=n_identical/n_aligned= 0.810
                data = line.split(",")
                #print([data], [split_key])
                #print(data[1].split(split_key))
                #print(data)
                #print()
                
                _dict["Aligned length="] = data[0].split(split_key)[1].replace(" ", "")
                _dict["RMSD="] = data[1].split(split_key)[1].replace(" ", "")
                _dict["Seq_ID=n_identical/n_aligned="] = data[2].split(split_key)[2].replace(" ", "").strip()
                break
            elif item == "TM-score=":
                #TM-score= 0.72182 (if normalized by length of Chain_1)
                #TM-score= 0.72182 (if normalized by length of Chain_2)
                #TM-score= 0.72182 (if normalized by average length of chains = 341.0)
                current_line = line
                data = current_line.split(split_key)
                value = data[1].split(" ")[1]
                #print(value)
                if "Chain_1" in current_line:
                    _dict["Normalized_Chain_1_TM_Score"] = value
                elif "Chain_2" in current_line:
                    _dict["Normalized_Chain_2_TM_Score"] = value
                elif "average" in current_line:
                    _dict["Normalized_Average_TM_Score"] = value
                else:
                    pass
                #end if
                break
            else:
                current_line = line
                data = current_line.split(split_key)
                _dict[item] = data[1].strip()
            #end if

        #end if
    #end for
    return _dict

#end method

# --- Main ---
parsed_results = {}

for data in tqdm(data_files):
    #print("# Processing file:", data)
    
    with open(data, "r") as tmalign_file:
        lines = tmalign_file.readlines()
    #end with

    # Initialize dict
    parsed_results[count] = data_dict.copy()
    
    for line in lines:
       parsed_results[count] = process(line,
                                       parsed_results[count])
    #end for

    try:
        del parsed_results[count]["TM-score="]
        #parsed_results[count]["RMSD"] = parsed_results[count].pop("RMSD=")
    except:
        pass
    #end try
    
    count += 1
    

#end for

#print(parsed_results)

# convert to df
df = pd.DataFrame.from_dict(parsed_results, orient="index")

# save df
                               
#if not os.path.isfile(output_csv):
#    #print("# Saving - first time")
#    df.to_csv(output_csv, index=True, header=True)
#else:
#    #print("# Saving in append mode")
#    df.to_csv(output_csv, mode='a', index=True, header=False)
#end if
 
print("# Saving table to:", output_csv)
df.to_csv(output_csv, index=True, header=True)
 
# --- End of file ---

