
mkdir -p UncompressedFiles

cd CompressedFiles

for zf in $(ls *.zip); do
    unzip -o $zf -d ../UncompressedFiles;
done

cd ..
