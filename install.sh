#! /bin/bash

echo "Installing Nim-NN..."

git clone git@github.com:astro-musician/Nim_NN.git

cd Nim_NN

bash makepyenv.sh

echo "------------------------------"
echo "To run the program, type either :" 
echo "bash Nim-NN.sh"
echo "or :"
echo "source .NimNN-env/bin/activate"
echo "python3 __main__.py"
echo "------------------------------"
echo "To change language, modify the language variable in __main__.py"