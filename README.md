![CI](https://github.com/rajputakhil/germline-mini/actions/workflows/ci.yml/badge.svg)


# germline-mini — sprint starter kit

A small Nextflow DSL2 pipeline (FASTQ → fastp → BWA-MEM2 → MarkDuplicates → DeepVariant → hap.py vs GIAB)
plus the Week 2 BQSR/HaplotypeCaller exercise, a confidence-interval script, drills and CI.
Everything runs today in **stub mode** (no tools, no data) so you can learn the wiring first,
then swap in real containers and data.

```bash
nextflow run main.nf -profile test -stub          # wiring check, ~10 s
nf-test test --profile test                       # process + pipeline tests
python bin/benchmark_ci.py results/benchmark/HG002.summary.csv
python -m pytest exercises -q                     # your drills (fail until you write them)
DRILLS=exercises.solutions.genomics_drills python -m pytest exercises -q   # answer key
python exercises/sql_drills.py                    # SQL drills (--solutions to see answers)
```

## Going real (week 1–2)
1. Download GRCh38 (analysis set, no alts), `samtools faidx`, `bwa-mem2 index`, `gatk CreateSequenceDictionary`.
2. HG002 reads: pick a WGS FASTQ from the GIAB data indexes, then downsample / restrict to chr20.
3. Truth: GIAB `NISTv4.2.1/GRCh38` HG002 VCF + BED; stratifications v3.1 for per-context results.
4. Build a bwa-mem2 + samtools image (or use a biocontainers mulled image) and set it in `modules/bwa_mem2.nf`.
5. Set `--model_type WGS` vs `WES` in `modules/deepvariant.nf` to match your data.
6. Run with `-profile docker` and real `--fasta --truth_vcf --truth_bed --samplesheet`.

## Validation README template (week 3)
Purpose & scope · Reference materials (GIAB version, regions) · Pipeline version & containers ·
Results table with 95% CIs by variant type and stratum · Known limitations (homopolymers, segdups,
PMS2/SMN1) · Cost per sample & runtime (from `results/pipeline_info/trace.txt`) · Change-control note.
