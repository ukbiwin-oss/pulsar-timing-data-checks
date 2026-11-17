#!/usr/bin/env python3
"""EPTA DR2: where the bin dictionaries and the per-pulsar noise files disagree.  (17 November 2026)

For each of the four data sets, red_dict.json, dm_dict.json and chrom_dict.json give, per pulsar, the number of
frequency bins of the red, DM and chromatic (scattering) processes, or null.  <psr>_noise.json gives noise values.
Prints every pulsar where a process has bins but no amplitude or slope in the noise file, and the exponential-dip
keys in J1713+0747's file.
Read the README before drawing conclusions: the release describes the per-pulsar files as white-noise files, and
its own scripts fit the other processes freely, so most of what this prints is intended.
Usage: python3 02_epta_noise_terms.py <path to EPTA-DR2/noisefiles>
"""
import json, os, sys
ROOT = sys.argv[1]
TERMS = (('red_dict.json', ('red_noise', '_rn_')), ('dm_dict.json', ('dm_gp',)), ('chrom_dict.json', ('_cn_',)))
for ds in sorted(os.listdir(ROOT)):
    d = os.path.join(ROOT, ds)
    if not os.path.isdir(d): continue
    print(f'{ds}:')
    for dictfile, words in TERMS:
        bins = json.load(open(os.path.join(d, dictfile)))
        for psr, n in sorted(bins.items()):
            keys = json.load(open(os.path.join(d, f'{psr}_noise.json')))
            have = [k[len(psr) + 1:] for k in keys if any(w in k for w in words)]
            if n is not None and not have: print(f'   {psr}: {dictfile} gives {n} bins, but {psr}_noise.json has no parameter of that process')
            if n is None and have: print(f'   {psr}: {dictfile} gives null, but {psr}_noise.json has {have}')
    keys = json.load(open(os.path.join(d, 'J1713+0747_noise.json')))
    dips = [k[len('J1713+0747_'):] for k in keys if 'expd' in k]
    print(f'   J1713+0747_noise.json: {len(keys)} keys; exponential-dip keys: {dips}')
