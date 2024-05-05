# SPA-REM2

## Description

Our application Structural assessment of Proteins using Ancestral sequence reconstruction (SPA) is designed to examine the evolutionary history of a protein.

## Initial setup by the user.

Place the SLAC json in the data folder `mammalian_REM2_codons.SA.FilterOutliers.fasta.SLAC.json`

Place clade data from the AOC-Rem2 analysis (*.clade files) in to the `data/clade_files` folder.

Place the labelled newick tree ("mammalian_REM2_codons.SA.FilterOutliers.fasta.treefile.labelled") from the AOC-Rem2 analysis in the 'data' folder 

## SPA Workflow 

### Before Colabfold

run `run_AncestralEvolution.sh`
. This creates: \ 
.. mammalian_REM2_codons.SA.FilterOutliers.fasta.SLAC.json.aa.fasta \
.. mammalian_REM2_codons.SA.FilterOutliers.fasta.SLAC.json.dna.fasta \ 
.. mammalian_REM2_codons.SA.FilterOutliers.fasta.SLAC.json.msa.fasta \

run `runTN93.sh` on the MSA fasta file to get TN93 genetic distances.

run `seqkitSplitByID.sh`
. This creates:
.. The folder `mammalian_REM2_codons.SA.FilterOutliers.fasta.SLAC.json.aa.fasta.split` which contains 1 FASTA file per species, with 1 protein sequence inside of the FASTA file.

### Colabfold

These are now ran through ColabFold to get the inferred protein structures. Results are downloaded, and PDB structures (Only Rank 1), are used for downstream analyses and placed in the 'results/PDB_Rank1' folder

### After Colabfold

run `run_TMAlign.sh` to get the TM-Align scores. These are placed in the `results/TMAlignResults` folder as .txt files.

run `scripts/tm_align_parser.py`, this generates `tables/TM_Align_Results.csv`

run `notebooks/Combined_GeneticDistance_TMAlign_Analysis_Complete.py`.. this generates `tables/TM_Align_Results_with_GeneticDistance-Complete.csv`

The labelled newick tree ("mammalian_REM2_codons.SA.FilterOutliers.fasta.treefile.labelled") may need a semicolon ";" added to the end of it, to make it a correct newick formatted file.

run `notebooks/ReadTree.py`.

## Visualization

run `notebooks/modelAdjustPairNames.py`. This creates the CSV file used for visualization.

run `notebooks/viewAdjustPairNames.py`.