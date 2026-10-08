#!/usr/bin/env nextflow
// Germline mini-pipeline: FASTQ -> BAM -> VCF -> hap.py benchmark
params.samplesheet = 'assets/samplesheet.csv'   // sample,fastq_1,fastq_2
params.fasta       = null                       // GRCh38 FASTA (+ .fai, bwa-mem2 index alongside)
params.truth_vcf   = null                       // GIAB NISTv4.2.1 HG002 VCF
params.truth_bed   = null                       // GIAB confident regions BED
params.regions     = 'chr20'
params.outdir      = 'results'

// modules see params defined above this line
include { FASTP       } from './modules/fastp'
include { BWA_MEM2    } from './modules/bwa_mem2'
include { MARKDUP     } from './modules/markdup'
include { DEEPVARIANT } from './modules/deepvariant'
include { HAPPY       } from './modules/happy'

// FASTQ paths in the sheet may be absolute, s3://, or relative to the sheet itself
def resolveFastq(sheet, String p) {
    (p.startsWith('/') || p.contains('://')) ? file(p, checkIfExists: true) : file("${sheet.parent}/${p}", checkIfExists: true)
}

workflow {
    def sheet = file(params.samplesheet, checkIfExists: true)
    def reads = channel.fromPath(sheet)
        .splitCsv(header: true)
        .map { row -> tuple([id: row.sample], resolveFastq(sheet, row.fastq_1), resolveFastq(sheet, row.fastq_2)) }

    def ref = channel.value(file(params.fasta))

    def bwa_index = channel.value(files("${params.fasta}.{0123,amb,ann,bwt.2bit.64,pac}"))
    FASTP(reads)
    BWA_MEM2(FASTP.out.reads, ref, bwa_index)
    MARKDUP(BWA_MEM2.out.bam)
    if (!params.skip_calling) {          // --skip_calling: stop after MARKDUP (Week 1)
        DEEPVARIANT(MARKDUP.out.bam, ref)
        HAPPY(DEEPVARIANT.out.vcf, ref, file(params.truth_vcf), file(params.truth_bed))
    }
}
