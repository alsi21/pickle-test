#! /usr/bin/bash
echo "Start test"
conda  --version
rm -f output.txt

# Python version 3.9
conda create --name py39 python=3.9 --yes
source activate py39
python3 test_script.py
conda deactivate

# Python version 2.7
conda create --name py27 python=2.7 --yes
source activate py27
python2 test_script.py
conda deactivate