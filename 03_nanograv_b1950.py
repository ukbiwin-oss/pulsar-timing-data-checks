#!/usr/bin/env python3
"""NANOGrav 15-yr analysis products: the direction 'pos' stored with each pulsar.  (17 November 2026)

Each feather file holds a direction 'pos' in its metadata and a direction per arrival time in columns pos_t_*.
For every pulsar: the angle between the two.  For those that differ by more than 1 arcsecond: the direction from
the release par file's ecliptic coordinates converted as enterprise does it (pulsar.py, _get_radec_from_ecliptic: pyephem,
epoch "1950" if the name contains "B", else "2000"), with both epochs.
Usage: python 03_nanograv_b1950.py <folder with the feather files> <folder with the narrowband par files>
Needs numpy, pyarrow and ephem (pyephem).
"""
import glob, json, os, sys
import numpy as np, pyarrow.feather as pf
from ephem import Ecliptic, Equatorial
FEATHERS, PAR = sys.argv[1], sys.argv[2]
def angle(a, b): return np.degrees(np.arctan2(np.linalg.norm(np.cross(a, b)), np.dot(a, b)))
def from_ecliptic(elong_deg, elat_deg, epoch):
    eq = Equatorial(Ecliptic(np.radians(elong_deg), np.radians(elat_deg)), epoch=epoch)
    ra, dec = float(eq.ra), float(eq.dec)
    return np.array([np.cos(ra) * np.cos(dec), np.sin(ra) * np.cos(dec), np.sin(dec)])
files = sorted(glob.glob(os.path.join(FEATHERS, '*.feather'))); off = []
for f in files:
    t = pf.read_table(f, columns=['pos_t_0', 'pos_t_1', 'pos_t_2']); meta = json.loads(t.schema.metadata[b'json'])
    pos_t = np.array([np.mean(t[c].to_numpy()) for c in t.column_names]); a = angle(np.array(meta['pos']), pos_t)
    if a > 1 / 3600: off.append((meta['name'], a, np.array(meta['pos']), pos_t))
print(f'{len(files)} feather files; "pos" and pos_t differ by more than 1 arcsecond in {len(off)}:')
for name, a, pos, pos_t in off:
    par = glob.glob(os.path.join(PAR, name + '_PINT_*.nb.par'))[0]
    v = {w[0]: float(w[1]) for w in (l.split() for l in open(par)) if w and w[0] in ('ELONG', 'ELAT')}
    p50, p00 = from_ecliptic(v['ELONG'], v['ELAT'], '1950'), from_ecliptic(v['ELONG'], v['ELAT'], '2000')
    print(f'   {name}: pos against pos_t {a:.4f} deg; pos against par direction with epoch "1950" {angle(pos, p50) * 3600:.2e} arcsec;'
          f' pos_t against par direction with epoch "2000" {angle(pos_t, p00) * 3600:.2e} arcsec')
