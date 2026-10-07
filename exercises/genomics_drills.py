"""Sprint coding drills. Fill in each function, then run:  python -m pytest exercises -q
Aim for 20 minutes per drill; compare with exercises/solutions/ only after the tests pass or time runs out."""

def merge_intervals(intervals):
    """[(1,5),(3,8),(10,12)] -> [(1,8),(10,12)]. Half-open intervals; touching ones (5,5) merge."""
    

def reciprocal_overlap(a, b):
    """Fraction of overlap relative to the LONGER of the two intervals (i.e. the min of both fractions)."""
    

def matches(a, b, threshold=0.5):
    """True if the two CNVs meet the reciprocal-overlap threshold."""
    

def titv(vcf_lines):
    """Ti/Tv over biallelic SNVs in VCF text lines. A<->G and C<->T are transitions."""
    

def het_hom_ratio(gts):
    """Het / hom-alt count from GT strings like '0/1', '1|1', './.'. Skip missing and hom-ref."""
    

def coverage_summary(depths, min_depth=20):
    """Return (mean depth, fraction of bases >= min_depth)."""
    
