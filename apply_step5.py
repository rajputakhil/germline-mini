#!/usr/bin/env python3
"""Step 5 edits for germline-mini. Run from the kit folder: python3 apply_step5.py
Safe to run twice. Keeps a .bak copy of every file it changes."""
import re, shutil, pathlib, sys

def edit(path, fn):
    p = pathlib.Path(path)
    old = p.read_text()
    new = fn(old)
    if new != old:
        shutil.copy(p, str(p) + ".bak")
        p.write_text(new)
        print(f"  changed  {path}")
    else:
        print(f"  ok       {path} (already done)")

def main_nf(s):
    if "bwa_index" not in s:
        m = re.search(r"^([ \t]*)((?:def )?)ref\s*=\s*channel\.value\(file\(params\.fasta\)\)\s*$", s, re.M)
        if not m: sys.exit("main.nf: could not find the 'ref = channel.value(file(params.fasta))' line")
        ind, d = m.group(1), m.group(2)
        line = f'\n{ind}{d}bwa_index = channel.value(files("${{params.fasta}}.{{0123,amb,ann,bwt.2bit.64,pac}}"))'
        s = s[:m.end()] + line + s[m.end():]
    s = s.replace("BWA_MEM2(FASTP.out.reads, ref)", "BWA_MEM2(FASTP.out.reads, ref, bwa_index)")
    if "skip_calling" not in s:
        m = re.search(r"^([ \t]*)(DEEPVARIANT\(.*\)\s*\n)[ \t]*(HAPPY\(.*\)\s*\n)", s, re.M)
        if not m: sys.exit("main.nf: could not find the DEEPVARIANT and HAPPY lines")
        ind = m.group(1)
        block = (f"{ind}if (!params.skip_calling) {{          // --skip_calling: stop after MARKDUP (Week 1)\n"
                 f"{ind}    {m.group(2)}{ind}    {m.group(3)}{ind}}}\n")
        s = s[:m.start()] + block + s[m.end():]
    return s

def bwa_nf(s):
    if "path index" not in s:
        s = re.sub(r"^([ \t]*)path fasta[^\n]*\n", lambda m: m.group(0) + f"{m.group(1)}path index      // bwa-mem2 index files, staged next to the FASTA\n", s, count=1, flags=re.M)
    s = re.sub(r"container '[^']*'", "container 'germline-mini/bwa-mem2-samtools:2.2.1'", s, count=1)
    return s

def config(s):
    if "skip_calling" not in s:
        s = "params.skip_calling = false   // true = FASTP -> BWA_MEM2 -> MARKDUP only\n" + s
    if "runOptions" not in s:
        new = ("docker {\n        docker.enabled = true\n"
               "        docker.runOptions = '-u $(id -u):$(id -g)'        // output files owned by you, not root\n"
               "        process.resourceLimits = [cpus: 4, memory: 8.GB]   // fit your laptop (nproc, free -g)\n    }")
        s, n = re.subn(r"docker\s*\{\s*docker\.enabled\s*=\s*true\s*\}", new, s, count=1)
        if not n: sys.exit("nextflow.config: could not find the docker profile")
    return s

for f in ["main.nf", "modules/bwa_mem2.nf", "nextflow.config"]:
    if not pathlib.Path(f).exists(): sys.exit(f"{f} not found: run this from inside ~/germline-mini")
print("Editing pipeline files:")
edit("main.nf", main_nf)
edit("modules/bwa_mem2.nf", bwa_nf)
edit("nextflow.config", config)

df = pathlib.Path("containers/bwa-mem2/Dockerfile")
df.parent.mkdir(parents=True, exist_ok=True)
df.write_text("FROM ubuntu:26.04\n"
              "RUN apt-get update && apt-get install -y --no-install-recommends bwa-mem2 samtools procps \\\n"
              " && rm -rf /var/lib/apt/lists/*\n")
print(f"  wrote    {df}")
for ext in ["0123", "amb", "ann", "bwt.2bit.64", "pac"]:
    pathlib.Path(f"tests/data/ref.fa.{ext}").touch()
print("  wrote    tests/data/ref.fa.{0123,amb,ann,bwt.2bit.64,pac} (empty placeholders for CI)")
print("Done. Next: nextflow run main.nf -profile test -stub")
