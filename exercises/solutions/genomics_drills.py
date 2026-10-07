"""Reference solutions for the sprint coding drills. Try exercises/genomics_drills.py first."""
from collections import Counter

# 1. Merge overlapping intervals (half-open [start, end)).
def merge_intervals(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return [tuple(x) for x in out]

# 2. Reciprocal overlap between two CNVs on the same chromosome.
def reciprocal_overlap(a, b):
    ov = max(0, min(a[1], b[1]) - max(a[0], b[0]))
    if ov == 0:
        return 0.0
    return min(ov / (a[1] - a[0]), ov / (b[1] - b[0]))

def matches(a, b, threshold=0.5):
    return reciprocal_overlap(a, b) >= threshold

# 3. Ti/Tv ratio from VCF lines (biallelic SNVs only).
TRANSITIONS = {frozenset("AG"), frozenset("CT")}

def titv(vcf_lines):
    ti = tv = 0
    for line in vcf_lines:
        if line.startswith("#"):
            continue
        ref, alt = line.split("\t")[3:5]
        if len(ref) != 1 or len(alt) != 1 or alt == "*":
            continue
        if frozenset(ref + alt) in TRANSITIONS:
            ti += 1
        else:
            tv += 1
    return ti / tv if tv else float("inf")

# 4. Het/hom-alt ratio from GT strings.
def het_hom_ratio(gts):
    c = Counter()
    for gt in gts:
        a = gt.replace("|", "/").split("/")
        if "." in a:
            continue
        if a[0] != a[1]:
            c["het"] += 1
        elif a[0] != "0":
            c["hom"] += 1
    return c["het"] / c["hom"] if c["hom"] else float("inf")

# 5. Mean depth and % bases >= 20x from a per-base depth list.
def coverage_summary(depths, min_depth=20):
    n = len(depths)
    return sum(depths) / n, sum(d >= min_depth for d in depths) / n
