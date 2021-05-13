printf "\nfile rights of testfile.txt:\n"
ls -alh testfile.txt

printf "\ncat content of testfile.txt:\n"
cat testfile.txt

printf "\noverwrite content of testfile.txt:\n"
echo "new content" > testfile.txt

printf "\nexcecute testfile.txt:\n"
./testfile.txt