#!/usr/bin/env python3
"""How much do the three 1950-epoch directions change the Hellings-Downs template?  (17 November 2026)

For each of the three affected pulsars and each of the other pulsars: the angular separation computed from the
stored direction 'pos' and from the per-arrival-time direction pos_t (mean), and the Hellings-Downs value for both.
Usage: python 04_hellings_downs_shift.py <folder with the feather files>
Needs numpy and pyarrow.
"""
import glob, json, os, sys
import numpy as np, pyarrow.feather as pf
def hd(cosz):
    x = (1 - cosz) / 2
    return 1.5 * x * np.log(x) - x / 4 + 0.5
pos, post = {}, {}
for f in sorted(glob.glob(os.path.join(sys.argv[1], '*.feather'))):
    t = pf.read_table(f, columns=['pos_t_0', 'pos_t_1', 'pos_t_2']); m = json.loads(t.schema.metadata[b'json'])
    pos[m['name']] = np.array(m['pos']); v = np.array([np.mean(t[c].to_numpy()) for c in t.column_names]); post[m['name']] = v / np.linalg.norm(v)
bad = [n for n in pos if np.degrees(np.arccos(np.clip(pos[n] @ post[n], -1, 1))) > 1 / 3600]
print(f'{len(pos)} pulsars; affected: {bad}')
worst_h = worst_a = 0.0
for a in bad:
    for b in pos:
        if b == a: continue
        c0, c1 = pos[a] @ pos[b], post[a] @ post[b]
        dang = abs(np.degrees(np.arccos(c0)) - np.degrees(np.arccos(c1))); dh = abs(hd(c0) - hd(c1))
        if b in bad: print(f'   {a} - {b}: separation changes by {dang:.4f} deg, Hellings-Downs value by {dh:.1e}')
        else: worst_h, worst_a = max(worst_h, dh), max(worst_a, dang)
print(f'   pairs of an affected with an unaffected pulsar ({len(bad) * (len(pos) - len(bad))}): largest change of separation {worst_a:.3f} deg, of the Hellings-Downs value {worst_h:.4f}')
