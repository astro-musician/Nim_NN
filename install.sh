#! /bin/bash

echo "Installing Nim-NN..."

git clone git@github.com:astro-musician/Nim_NN.git

cd Nim_NN
mkdir nn_saves

python3 -m venv .NimNN-env
source .NimNN-env/bin/activate
pip install numpy
pip install matplotlib
pip install progressbar
pip install PyQt6

echo "------------------------------"
echo "To run the program, type either :" 
echo "bash Nim-NN.sh"
echo "or :"
echo "source .NimNN-env/bin/activate"
echo "python3 __main__.py"
echo "------------------------------"
echo "To change language, modify the language variable in __main__.py"