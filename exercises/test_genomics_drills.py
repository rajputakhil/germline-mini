import importlib, os, pytest
MOD = os.environ.get("DRILLS", "exercises.genomics_drills")   # DRILLS=exercises.solutions.genomics_drills to check the key
d = importlib.import_module(MOD)

def test_merge():
    assert d.merge_intervals([(10, 12), (1, 5), (3, 8)]) == [(1, 8), (10, 12)]
    assert d.merge_intervals([(1, 5), (5, 7)]) == [(1, 7)]
    assert d.merge_intervals([]) == []

def test_reciprocal_overlap():
    assert d.reciprocal_overlap((0, 100), (50, 150)) == pytest.approx(0.5)
    assert d.reciprocal_overlap((0, 100), (10, 20)) == pytest.approx(0.1)   # small CNV inside a big one
    assert d.reciprocal_overlap((0, 10), (20, 30)) == 0
    assert d.matches((0, 100), (40, 140)) and not d.matches((0, 100), (10, 20))

VCF = """##fileformat=VCFv4.2
#CHROM\tPOS\tID\tREF\tALT
chr20\t1\t.\tA\tG
chr20\t2\t.\tC\tT
chr20\t3\t.\tA\tC
chr20\t4\t.\tAT\tA
chr20\t5\t.\tG\tA""".splitlines()

def test_titv():
    assert d.titv(VCF) == pytest.approx(3.0)

def test_het_hom():
    assert d.het_hom_ratio(["0/1", "1|1", "0/0", "./.", "0|1", "1/2", "1/1"]) == pytest.approx(1.5)

def test_coverage():
    mean, frac = d.coverage_summary([10, 20, 30, 40])
    assert mean == 25 and frac == 0.75
