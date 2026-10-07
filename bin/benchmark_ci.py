#!/usr/bin/env python3
"""Add 95% confidence intervals to a hap.py summary.csv.

Recall    = TRUTH.TP / (TRUTH.TP + TRUTH.FN)
Precision = QUERY.TP / (QUERY.TP + QUERY.FP), with QUERY.TP = QUERY.TOTAL - QUERY.FP - QUERY.UNK

Usage: benchmark_ci.py HG002.summary.csv [--filter PASS] > metrics_ci.tsv
"""
import argparse
import csv
import sys

from statsmodels.stats.proportion import proportion_confint


def ci(successes: int, n: int, method: str) -> tuple[float, float]:
    """Two-sided 95% CI for a binomial proportion ('wilson' or 'beta' = Clopper-Pearson)."""
    lo, hi = proportion_confint(successes, n, alpha=0.05, method=method)
    return float(lo), float(hi)


def rows_with_ci(rows, filt="PASS"):
    for r in rows:
        if r["Filter"] != filt:
            continue
        ttp, tfn = int(r["TRUTH.TP"]), int(r["TRUTH.FN"])
        qfp = int(r["QUERY.FP"])
        qtp = int(r["QUERY.TOTAL"]) - qfp - int(r.get("QUERY.UNK", 0) or 0)
        rec, prec = ttp / (ttp + tfn), qtp / (qtp + qfp)
        yield {
            "type": r["Type"],
            "recall": rec,
            "recall_wilson": ci(ttp, ttp + tfn, "wilson"),
            "recall_cp": ci(ttp, ttp + tfn, "beta"),
            "precision": prec,
            "precision_wilson": ci(qtp, qtp + qfp, "wilson"),
            "precision_cp": ci(qtp, qtp + qfp, "beta"),
            "f1": 2 * rec * prec / (rec + prec),
        }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("summary_csv")
    ap.add_argument("--filter", default="PASS")
    a = ap.parse_args()
    with open(a.summary_csv) as fh:
        out = list(rows_with_ci(csv.DictReader(fh), a.filter))
    w = sys.stdout.write
    w("type\trecall\trecall_95CI_wilson\trecall_95CI_clopper_pearson\tprecision\tprecision_95CI_wilson\tF1\n")
    f = lambda t: f"{t[0]:.4f}-{t[1]:.4f}"
    for o in out:
        w(f"{o['type']}\t{o['recall']:.4f}\t{f(o['recall_wilson'])}\t{f(o['recall_cp'])}\t"
          f"{o['precision']:.4f}\t{f(o['precision_wilson'])}\t{o['f1']:.4f}\n")


if __name__ == "__main__":
    main()
