#!/usr/bin/env python3
"""PPTA DR3: which released par files have a position that is not fitted?  (17 November 2026)

A tempo2 par line is "NAME value [fit flag] [error]"; fit flag 1 means the parameter is fitted.
Prints, for every par file in each folder of the release, the position parameters without fit flag 1.
Usage: python3 01_ppta_frozen_position.py <path to ppta_dr3/toas_and_parameters>
"""
import glob, os, sys
ROOT = sys.argv[1]
POS = ('RAJ', 'DECJ', 'ELONG', 'ELAT', 'LAMBDA', 'BETA')
for folder in sorted(os.listdir(ROOT)):
    pars = sorted(glob.glob(os.path.join(ROOT, folder, '*.par')))
    if not pars: continue
    frozen = []
    for p in pars:
        for n, line in enumerate(open(p), 1):
            w = line.split()
            if w and w[0] in POS and not (len(w) >= 3 and w[2] == '1'):
                frozen.append(f'      {os.path.basename(p)} line {n}: {line.rstrip()}')
    print(f'{folder}/: {len(pars)} par files; position lines without fit flag: {len(frozen)}')
    print('\n'.join(frozen)) if frozen else None
