"""Round a night plan x.csv (from lp_model.py) to whole bikes.

Each x[i,j] is rounded to the nearest integer (half to even, numpy.round);
pairs that round to 0 are dropped. The rounded plan can then be evaluated
with `lp_model.py --plan <out>/x.csv`, which keeps x fixed and solves only
the day part (served and lost trips).

Usage:
    python round_plan.py --plan reports/lp/weekday_p3.5_R1.5_alpha0.5/x.csv \
        --out reports/lp/rounded_weekday_p3.5
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plan", required=True, help="x.csv written by lp_model.py")
    ap.add_argument("--out", required=True, help="folder for the rounded x.csv")
    args = ap.parse_args()

    x = pd.read_csv(args.plan)
    r = x.assign(x=np.round(x["x"]))
    r = r[r["x"] > 0]

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    r.to_csv(out / "x.csv", index=False)
    print(f"pairs {len(x)} -> {len(r)}, bikes {x['x'].sum():,.1f} -> {r['x'].sum():,.0f}")
    print(f"wrote {out / 'x.csv'}")


if __name__ == "__main__":
    main()
