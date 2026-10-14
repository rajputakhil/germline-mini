#!/usr/bin/env python3
"""Week 2, step 6 edits for germline-mini (DeepVariant on real data).
Run from the kit folder: python3 apply_step6.py   Safe to run twice; keeps .bak copies."""
import re, shutil, pathlib, sys

def edit(path, fn):
    p = pathlib.Path(path); old = p.read_text(); new = fn(old)
    if new != old:
        shutil.copy(p, str(p) + ".bak"); p.write_text(new); print(f"  changed  {path}")
    else:
        print(f"  ok       {path} (already done)")

def main_nf(s):
    if "bwa_index" not in s or "skip_calling" not in s:
        sys.exit("main.nf: run apply_step5.py first (Week 1 changes are missing)")
    if "params.fasta}.fai" not in s:
        m = re.search(r"^([ \t]*)((?:def )?)bwa_index\s*=.*$", s, re.M)
        s = s[:m.end()] + f'\n{m.group(1)}{m.group(2)}fai = channel.value(file("${{params.fasta}}.fai"))   // DeepVariant needs the FASTA index staged too' + s[m.end():]
    s = s.replace("DEEPVARIANT(MARKDUP.out.bam, ref)", "DEEPVARIANT(MARKDUP.out.bam, ref, fai)")
    if "skip_benchmark" not in s:
        m = re.search(r"^([ \t]*)(HAPPY\(.*\)\s*\n)", s, re.M)
        if not m: sys.exit("main.nf: could not find the HAPPY line")
        ind = m.group(1)
        s = s[:m.start()] + (f"{ind}if (!params.skip_benchmark) {{     // --skip_benchmark: stop after DeepVariant\n"
                             f"{ind}    {m.group(2)}{ind}}}\n") + s[m.end():]
    return s

def dv_nf(s):
    s = s.replace("--model_type=WES", "--model_type=${params.dv_model}")
    if "path fai" not in s:
        s = re.sub(r"^([ \t]*)path fasta[^\n]*\n", lambda m: f"{m.group(1)}path fasta\n{m.group(1)}path fai     // chr20.fa.fai, staged next to the FASTA\n", s, count=1, flags=re.M)
    return s

def config(s):
    add = ""
    if "params.dv_model" not in s: add += "params.dv_model = 'WGS'           // DeepVariant model: WGS for whole-genome data, WES for exomes\n"
    if "skip_benchmark" not in s:  add += "params.skip_benchmark = false     // true = stop after DeepVariant (no hap.py)\n"
    return add + s

for f in ["main.nf", "modules/deepvariant.nf", "nextflow.config"]:
    if not pathlib.Path(f).exists(): sys.exit(f"{f} not found: run this from inside ~/germline-mini")
print("Editing pipeline files:")
edit("main.nf", main_nf)
edit("modules/deepvariant.nf", dv_nf)
edit("nextflow.config", config)
pathlib.Path("tests/data/ref.fa.fai").touch()
print("  wrote    tests/data/ref.fa.fai (empty placeholder for CI)")
print("Done. Next: nextflow run main.nf -profile test -stub")
