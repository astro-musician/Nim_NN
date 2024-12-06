#! /bin/bash

echo "Installing Nim-NN..."

git clone git@github.com:astro-musician/Nim_NN.git

cd Nim_NN

python3 -m venv .NimNN-env
source activate .NimNN-env/bin/activate
pip install numpy
pip install matplotlib
pip install progressbar
pip install PyQt6

echo "To run the program, execute __main__.py"
echo "To change language, modify the language variable in __main__.py"