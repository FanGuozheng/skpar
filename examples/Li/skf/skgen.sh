#!/bin/bash

cd skf

rm -r _build/li/comp.*
# Use updated parameters to generate new skdefs.py
cp skdefs.py skdef.hsd

skgen -o slateratom -t sktwocnt sktable -d Li Li

mkdir -p Li/wavecomp
rm Li/wavecomp/*
cp _build/li/comp.*/wave_03[sp]* Li/wavecomp/

#mv Li-Li.skf LL && sed -i '1d' LL && sed -i '1d' LL
#cat Li-Li.py >> Li-Li.skf && cat LL >> Li-Li.skf

cd ..
