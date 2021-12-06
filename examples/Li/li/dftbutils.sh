#!/bin/bash

cd li
dftbutils bands -wd .
cd ..
cp li/bs/detailed.out .
cp li/bs/band.out .
cp li/bs/bands_tot.dat .
cp li/bs/dftb_pin.hsd .
