
BASEDIR=/Users/alex/Documents/SPA-REM2

cd $BASEDIR

# From the 'scripts' directory.
f=(results/PDB_Rank1/*.pdb)

OUTDIR="results/TMAlignResults"

mkdir -p $OUTDIR

for ((i = 0; i < ${#f[@]}; i++)); do
      for ((j = i + 1; j < ${#f[@]}; j++)); do
          #echo "${f[i]} - ${f[j]}";
        
          
          
          # "${firstString/Suzi/"$secondString"}"
          # mammalian_REM2_codons.SA.FilterOutliers.fasta.SLAC.json.aa.part_XM_052190525_1_PREDICTED_Apodemus_sylvaticus_RRAD_and_GEM_like_GTPase_2_LOC127690950_mRNA_1_unrelaxed_rank_001_alphafold2_ptm_model_1_seed_000.pdb
          # FOO=${FOO//"$WORDTOREMOVE"/}
          
          WORDTOREMOVE="mammalian_REM2_codons.SA.FilterOutliers.fasta.SLAC.json.aa.part_"
          WORDTOREMOVEALSO="_unrelaxed_rank_001_alphafold2_ptm_model_1_seed_000"
          
          b=$(basename -- "${f[j]}")
          #b="${$b/mammalian_REM2_codons.SA.FilterOutliers.fasta.SLAC.json.aa.part_/}"
          b=${b//"$WORDTOREMOVE"/}
          b=${b//"$WORDTOREMOVEALSO"/}
          
          a=$(basename -- "${f[i]}")
          #a="${$a/mammalian_REM2_codons.SA.FilterOutliers.fasta.SLAC.json.aa.part_/}"
          a=${a//"$WORDTOREMOVE"/}
          a=${a//"$WORDTOREMOVEALSO"/}
          
          OUTPUTFILE="$a"_AND_"$b"".txt"
          
          #if [ "${#OUTPUTFILE}" -ge 255 ]; then
          #   #Rename_file
          #   temp="${f[i]}_AND_${f[j]}.txt"
          #   temp2="${temp:0:250}.txt"
          #   OUTPUTFILE=$temp2
          #fi
          
          OUTPUT="$OUTDIR/$OUTPUTFILE"
          #echo "# TMAlign output saved to: "$OUTPUT
          
          #cmd="tmalign "${f[i]}" "${f[j]}" -a | tee $OUTPUT"
          echo $cmd
          echo ""
          eval $cmd
      done;
done

exit 0
