#!/usr/bin/env python3
"""Show a hap.py summary.csv as a confusion matrix per variant type.
Usage: python bin/confusion_matrix.py results/benchmark/HG002.summary.csv"""
import csv, sys

for r in csv.DictReader(open(sys.argv[1])):
    if r["Filter"] != "PASS":
        continue
    tp = int(r["TRUTH.TP"])
    fn = int(r["TRUTH.FN"])
    fp = int(r["QUERY.FP"])
    qtp = int(r["QUERY.TOTAL"]) - fp - int(r.get("QUERY.UNK") or 0)  # hap.py counts TPs on the call side too
    print(f"\n{r['Type']}")
    print(f"{'':22}{'Truth: variant':>16}{'Truth: no variant':>20}")
    print(f"{'Called: variant':22}{tp:>16,}{fp:>20,}   <- TP | FP")
    print(f"{'Not called':22}{fn:>16,}{'n/a':>20}   <- FN | TN")
    print(f"  Recall    = TP/(TP+FN) = {tp/(tp+fn):.4f}")
    print(f"  Precision = TP/(TP+FP) = {qtp/(qtp+fp):.4f}")
