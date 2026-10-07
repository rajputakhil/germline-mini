"""SQL drills on a tiny variant-reporting schema (SQLite, runs anywhere).
Write each query in QUERIES, then:  python exercises/sql_drills.py
Answers are in SOLUTIONS at the bottom; don't peek until you've tried."""
import sqlite3

SCHEMA = """
CREATE TABLE samples (sample_id TEXT PRIMARY KEY, test_code TEXT, received DATE, reported DATE);
CREATE TABLE variants (sample_id TEXT, gene TEXT, hgvs TEXT, classification TEXT, depth INT, vaf REAL);
INSERT INTO samples VALUES
 ('S1','WES','2026-09-01','2026-09-15'),('S2','WES','2026-09-02','2026-09-20'),
 ('S3','PANEL','2026-09-03','2026-09-08'),('S4','PANEL','2026-09-05','2026-09-19'),
 ('S5','WES','2026-09-06',NULL);
INSERT INTO variants VALUES
 ('S1','NRXN1','c.1A>G','VUS',45,0.48),('S1','SCN1A','c.2T>C','P',60,0.51),
 ('S2','SCN1A','c.2T>C','P',38,0.47),('S2','MECP2','c.3G>A','LP',12,0.22),
 ('S3','PMS2','c.4C>T','VUS',9,0.30),('S4','SCN1A','c.5del','LP',80,0.49),
 ('S4','GAA','c.6A>T','P',55,1.00);
"""

QUERIES = {
    # Q1. Turnaround time (days) per reported sample, plus the average TAT per test_code.
    "q1_tat": "-- your SQL here",
    # Q2. Genes with more than one P/LP variant across samples, most first.
    "q2_recurrent_genes": "-- your SQL here",
    # Q3. For each sample, its variant with the highest depth (window function: ROW_NUMBER).
    "q3_top_depth": "-- your SQL here",
    # Q4. Variants failing a QC rule: depth < 20 OR (vaf between 0.1 and 0.35) -- possible mosaic or artifact.
    "q4_qc_flags": "-- your SQL here",
}

SOLUTIONS = {
    "q1_tat": """
        SELECT sample_id, test_code,
               julianday(reported) - julianday(received) AS tat_days,
               AVG(julianday(reported) - julianday(received)) OVER (PARTITION BY test_code) AS avg_tat_by_test
        FROM samples WHERE reported IS NOT NULL ORDER BY sample_id""",
    "q2_recurrent_genes": """
        SELECT gene, COUNT(*) AS n_plp FROM variants
        WHERE classification IN ('P','LP') GROUP BY gene HAVING COUNT(*) > 1 ORDER BY n_plp DESC""",
    "q3_top_depth": """
        SELECT sample_id, gene, hgvs, depth FROM (
          SELECT *, ROW_NUMBER() OVER (PARTITION BY sample_id ORDER BY depth DESC) AS rn FROM variants)
        WHERE rn = 1 ORDER BY sample_id""",
    "q4_qc_flags": """
        SELECT sample_id, gene, hgvs, depth, vaf FROM variants
        WHERE depth < 20 OR vaf BETWEEN 0.1 AND 0.35 ORDER BY sample_id""",
}

if __name__ == "__main__":
    import sys
    con = sqlite3.connect(":memory:"); con.executescript(SCHEMA)
    use = SOLUTIONS if "--solutions" in sys.argv else QUERIES
    for name, sql in use.items():
        print(f"\n== {name}")
        if sql.strip().startswith("--"):
            print("(not written yet)"); continue
        cur = con.execute(sql)
        print([c[0] for c in cur.description])
        for row in cur: print(row)
