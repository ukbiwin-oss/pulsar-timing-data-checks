# Pulsar-timing data checks

Notes on six things met in three public pulsar-timing data sets, each checked before being stated. 17 November 2026. Unreviewed: no specialist in pulsar timing has read this.

The six turned up on 11 and 12 November 2026, during a test of how clocks on Earth respond to the gravity of the Sun and planets. That test is not published yet. On 17 November each item was reproduced, attacked, and compared with what the teams that publish the data have already documented.

The short result: **one stands as a small defect in released files, one is a question, two were already known to the teams, and two do not hold up.**

Nothing here is a criticism of the teams. All three releases are large, carefully documented, and public, which is the only reason checks like these are possible.

## 1. PPTA DR3: one pulsar's position is not fitted (stands)

Data: Parkes Pulsar Timing Array third data release, CSIRO Data Access Portal, DOI [10.25919/j4xr-wp05](https://doi.org/10.25919/j4xr-wp05) (version 2), folder `ppta_dr3/toas_and_parameters/all/`.

**What is in the file.** In `J1545-4550.par`, lines 2 and 3 (`ELONG` and `ELAT`, the pulsar's position) carry no fit flag. Of the 122 parameter files in the folders `all/`, `dr2/` and `uwl/`, it is the only one with an unflagged position (script 01).

The same pulsar's file in `dr2/` has the same values with fit flag 1 on both lines. The two files differ only in those two flags and in the wording of two `JUMP` lines.

**Why it matters.** A program that fits or marginalises only the flagged parameters leaves this pulsar's position fixed. The Sun's yearly clock term (0.83 milliseconds) is then not absorbed by the position, as it is for every other pulsar. In the clock test this one file produced a false "measurement" of that term, three times its error bar.

Tested with both common timing packages: tempo2 (through libstempo 2.5.1) fits no position parameter with this file, and PINT 1.1.8 freezes both.

**What limits it.** The release's README describes the basic files as less reliable than the noise-modelled ones, and the noise-modelled file for this pulsar (`J1545-4550_singlePsrNoise_fit.par`) does fit the position. So the PPTA's own analyses are probably not affected. That was not checked.

**A second, smaller item.** In `J1730-2304_singlePsrNoise_fit.par`, line 2, the fit flag of `ELONG` is `10`. The two packages read it differently: tempo2 still fits both coordinates, while PINT freezes `ELONG` and fits `ELAT`. It looks like a typing slip for `1`.

**Already known?** No erratum or note was found. The portal's current listing shows both files with the sizes of the copies used here (2,497 and 4,886 bytes), last changed in June 2023. It was reported by email to the contact named on the portal's collection record on 17 November 2026. Any reply will be noted here.

SHA-256 of the two files used: `cc6a129442d70442d64d1ec42e2b8b50f8f4b632d4be00604340daa51b38a9b4` and `d3f9e61083e2515a16c76321092af50e982f903115d1fd77c98e87094f28fc03`.

## 2. EPTA DR2: noise values "missing" from the noise files (mostly withdrawn; one question left)

Data: European Pulsar Timing Array second data release, `gitlab.in2p3.fr/epta/epta-dr2`, commit `2911d0e`, folder `noisefiles/`.

**What was first thought.** The release's bin dictionaries give J1600−3053 a chromatic (scattering) process and the papers give J1713+0747 two exponential dips, but the per-pulsar noise files for the full data set hold no values for either (script 02). This looked like an omission.

**Why that was wrong.** The release's README describes the per-pulsar files as white-noise files. The release's own analysis scripts fit the red, dispersion and chromatic processes freely, and add both of J1713+0747's dips explicitly (`scripts_gwb/os_run.py` and `model_comparison.py`: `num_dmdips` defaults to 2). The values are absent by design.

**What is left.** `red_dict.json` gives J2322+2057 ten red-noise bins in all four data sets. The EPTA's paper on the noise models (second DR2 paper, tables 4 and 5) lists that pulsar's model as "NONE": no time-correlated noise. The release scripts would therefore give it a red-noise term that the paper says the data do not support. The effect is probably small, and it may be deliberate. This is a question, not a defect.

On 17 November 2026 the question was emailed to the contact address given in the release's own pages. That address rejected the message, so the question has not yet reached the EPTA.

## 3. NANOGrav 15-year analysis files: three pulsars with directions half a degree off (real, already fixed upstream)

Data: `nanograv/15yr_stochastic_analysis`, commit `a3e8b87`, folder `tutorials/data/feathers/`; parameter files from the 15-year release v2.1.0.

**What is in the files.** Each file stores one direction for its pulsar (`pos`) and a direction for every arrival time (`pos_t`). For B1855+09, B1937+21 and B1953+29 the two differ by 0.59, 0.52 and 0.46 degrees. For the other 64 pulsars they agree to better than an arcsecond (script 03).

**Cause.** The stored direction equals, exactly, the parameter file's coordinates converted to the equator of 1950. The analysis package `enterprise` (version 3.5.0, `pulsar.py`) does this for any pulsar whose name contains "B". The coordinates in these parameter files are for the year 2000, so the conversion is not appropriate.

**Already known.** Yes. It is `enterprise` issue [#452](https://github.com/nanograv/enterprise/issues/452), opened in June 2026, and was fixed in the development branch by pull request [#453](https://github.com/nanograv/enterprise/pull/453), merged on 15 July 2026. As of 17 November 2026 the latest release is still 3.5.0 (14 July 2026) and the main branch still has the old code.

**Size of the effect.** `pos` sets the angle between pulsars in the expected correlation pattern of a gravitational-wave background (the Hellings-Downs curve). For the 192 pairs of an affected with an unaffected pulsar the pattern changes by at most 0.0073 (script 04). The three affected pulsars keep their angles to each other. This is far below what the present data can resolve.

No report is needed.

## 4. NANOGrav 15-year data: J1713+0747's two profile events (documented by the team)

Adding the pulsar's two known events (2008 and 2016) to its model as two terms with free sizes lowers its chi-squared by 81 at the published noise values.

This is not a defect. NANOGrav's 15-year papers describe both events and how the standard analysis treats them, and later NANOGrav work on the same data finds that this pulsar favours two event terms. The number also overstates the case, because the shapes of the terms were fitted elsewhere and the noise values were fitted without them.

The code for this item belongs to the unpublished clock test and is not included here.

## 5. EPTA DR2: a 430-day term in Nançay data (withdrawn)

A sinusoid of period 429.7 days common to the pulsars fitted at 33.5 ± 8.1 nanoseconds, mostly from Nançay data. It was first logged as unexplained.

It does not hold up:

- It is the largest of 97 periods scanned. The chance of one value that large somewhere among 97 is about 2 in 100 before any correction of the error bars, and larger after.
- In the Nançay data alone it is not a line. Two neighbouring periods (347 and 361 days) are stronger and two more (334 and 376 days) nearly as strong, so the excess is a broad band near one year. The clock test's own notes attribute most of that band to the solar wind.
- "Absent at the other telescopes" only reflects their larger error bars (7 ± 17 nanoseconds).

## 6. PPTA DR3: a near-annual term at Parkes shaped like Saturn's signal (withdrawn)

A common term with the time dependence of Saturn's gravitational potential fitted at −0.30 ± 0.09 of its predicted strength in Parkes data.

It does not hold up as a finding either. After calibrating the error bars it is between 2.4 and 2.95 standard deviations, and it is one of a dozen or more such values that were looked at. Parkes data show excess power at several periods near one year, and Saturn's shape is one of many that fit it.

## Files

| File | What it does |
|---|---|
| `01_ppta_frozen_position.py` | lists position lines without fit flag 1 in every PPTA DR3 parameter file |
| `02_epta_noise_terms.py` | lists where EPTA DR2's bin dictionaries and noise files disagree (read item 2 first) |
| `03_nanograv_b1950.py` | compares the stored direction with the per-arrival-time direction for all 67 pulsars |
| `04_hellings_downs_shift.py` | the change of the Hellings-Downs value from item 3 |
| `outputs.txt` | the output of the four scripts, 17 November 2026 |

Scripts 01 and 02 need only Python 3. Scripts 03 and 04 need numpy and pyarrow; 03 also needs ephem. Each takes the data folder as its argument (see the first lines of each file). The data are not included; they are public at the addresses above.

## What this is and is not

- Items 1 to 3 rest on the released files and can be re-run by anyone in seconds.
- Items 4 to 6 rest on an analysis that is not published yet, so they are reported here only as outcomes.
- "Already known" means a public issue, release note or paper was found and read. "Not found" does not prove that the teams are unaware.

## How it was made

Prepared by Lee Miller with Claude, an AI model made by Anthropic. Each item was examined by two AI agents in turn, the second instructed to refute the first, and the main claims were then re-checked by hand against the files and the sources linked above.

## Corrections

Corrections are welcome. Please open an issue, or write to research@lee-miller.com.
