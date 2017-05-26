#!/bin/bash
# this script calculates the two-center integrals
# and assembles the skf tables.
# It must be run in the optimisation loop since we
# are trying to optimise the compression radii

# NOTABENE: Do not rm skdefs.py within this script. 
# At this stage, it should be the one generated by the optimiser!

skgen potcomp -b slateratom C
# skgen potcomp -b slateratom C1

# now we skip the wavecomp computation, as we actually want the same 
# compression for both waves and density
# make dir if not present; do not complain if there
mkdir -p C/wavecomp
# mkdir -p C1/wavecomp
# clean if directory was there
/bin/rm -f C/wavecomp/*
# /bin/rm -f C1/wavecomp/*
# copy relevant files
/bin/cp C/potcomp/wave_02[sp].dat C/wavecomp/
# /bin/cp C1/potcomp/wave_02p.dat C1/wavecomp/
# /bin/cp C1/potcomp/wave_03s.dat C1/wavecomp/

# twocnt -g 0.2 is for grid spacing -s potential for superposition type
# the -m 14 is a must or else we have tables of different lengths for C and C1
# this is a problem for dftb+, since it has to use them for the same atom
# via SelectedShells. Hence we cut at the smallest length, which comes from
# the C-C skf.
skgen twocnt -g 0.2 -m 14 -s potential C  C
# skgen twocnt -g 0.2 -m 14 -s potential C1 C1
# skgen twocnt -g 0.2 -m 14 -s potential C  C1

# sktable -d is for dummy repulsive
skgen sktable -d C  C 
# skgen sktable -d C1 C1
# skgen sktable -d C  C1
# skgen sktable -d C1 C 
