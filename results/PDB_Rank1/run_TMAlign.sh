
# From the 'scripts' directory.
f=(*.pdb)

OUTDIR="../TMAlignResults"

mkdir -p $OUTDIR

count=0

#len=${#f[@]}

for ((i = 0; i < ${#f[@]}; i++)); do
      for ((j = i + 1; j < ${#f[@]}; j++)); do
          #echo "${f[i]} - ${f[j]}";
          # "${firstString/Suzi/"$secondString"}"
          # mammalian_REM2_codons.SA.FilterOutliers.fasta.SLAC.json.aa.part_XM_052190525_1_PREDICTED_Apodemus_sylvaticus_RRAD_and_GEM_like_GTPase_2_LOC127690950_mRNA_1_unrelaxed_rank_001_alphafold2_ptm_model_1_seed_000.pdb
          # FOO=${FOO//"$WORDTOREMOVE"/}
          
          WORDTOREMOVE="mammalian_REM2_codons.SA.FilterOutliers.fasta.SLAC.json.aa.part_"
          WORDTOREMOVEALSO="_unrelaxed_rank_001_alphafold2_ptm_model_1_seed_000"
          
          a=$(basename -- "${f[i]}")
          a=${a//"$WORDTOREMOVE"/}
          a=${a//"$WORDTOREMOVEALSO"/}
          
          b=$(basename -- "${f[j]}")
          b=${b//"$WORDTOREMOVE"/}
          b=${b//"$WORDTOREMOVEALSO"/}
          
          # Check if both files exist
          file1="$a"_AND_"$b"".txt"
          if [ -f "$OUTDIR/$file1" ]; then
            #echo "Warning! File does exist: $file1"
            continue
          fi
          file2="$b"_AND_"$a"".txt"

          if [ -f "$OUTDIR/$file2" ]; then
            #echo "Warning!! File does exist: $file2"
            continue
          fi
          #continue
          
          # Proceed
          OUTPUTFILE=$file1
          if [ "${#OUTPUTFILE}" -ge 255 ]; then
             #Rename_file
             #temp="${f[i]}_AND_${f[j]}.txt"
             #temp=$file1
             temp2="${file1:0:250}.txt"
             OUTPUTFILE=$temp2
          fi
        
          OUTPUT="$OUTDIR/$OUTPUTFILE"
          
          #echo "# TMAlign output saved to: "$OUTPUT
          cmd="tmalign "${f[i]}" "${f[j]}" -a | tee $OUTPUT"
          #cmd="tmalign "${f[i]}" "${f[j]}" -a > $OUTPUT"
          echo $cmd
          echo ""
          let count++
          eval $cmd
      done;
done

echo "FINAL COUNT: $count"
exit 0
