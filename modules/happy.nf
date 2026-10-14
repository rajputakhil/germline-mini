process HAPPY {
    tag "${meta.id}"
    container 'quay.io/biocontainers/hap.py:0.3.15--py27hcb73b3d_0'
    publishDir "${params.outdir}/benchmark", mode: 'copy'

    input:
    tuple val(meta), path(vcf), path(tbi)
    path fasta
    path fai          // chr20.fa.fai
    path truth_vcf
    path truth_tbi    // index for the truth VCF
    path truth_bed

    output:
    tuple val(meta), path("${meta.id}.summary.csv"), emit: summary
    path "${meta.id}.*",                             emit: all

    script:
    """
    hap.py ${truth_vcf} ${vcf} \\
      -f ${truth_bed} -r ${fasta} \\
      --threads ${task.cpus} -o ${meta.id}
    """

    stub:
    """
    printf 'Type,Filter,TRUTH.TOTAL,TRUTH.TP,TRUTH.FN,QUERY.TOTAL,QUERY.FP,QUERY.UNK,METRIC.Recall,METRIC.Precision,METRIC.F1_Score\\n' > ${meta.id}.summary.csv
    printf 'SNP,PASS,70000,69860,140,72000,95,2045,0.998,0.998641,0.99832\\nINDEL,PASS,11000,10890,110,11500,60,550,0.99,0.994521,0.992255\\n' >> ${meta.id}.summary.csv
    """
}
