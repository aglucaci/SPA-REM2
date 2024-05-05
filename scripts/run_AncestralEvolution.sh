

JSON="../data/mammalian_REM2_codons.SA.FilterOutliers.fasta.SLAC.json"

mkdir -p ../results

cmd="python ancestralevolution.py --slac_json $JSON --output_dna ../results/$JSON.dna.fasta --output_aa ../results/$JSON.aa.fasta --output_msa ../results/$JSON.msa.fasta"

echo $cmd

eval $cmd

exit 0

 
