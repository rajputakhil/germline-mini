process MARKDUP {
    tag "${meta.id}"
    container 'broadinstitute/gatk:4.6.1.0'
    publishDir "${params.outdir}/bam", mode: 'copy'

    input:
    tuple val(meta), path(bam)

    output:
    tuple val(meta), path("${meta.id}.md.bam"), path("${meta.id}.md.bai"), emit: bam
    path "${meta.id}.dup_metrics.txt",                                        emit: metrics

    script:
    """
    gatk MarkDuplicates -I ${bam} -O ${meta.id}.md.bam \\
         -M ${meta.id}.dup_metrics.txt --CREATE_INDEX true
    """

    stub:
    """
    touch ${meta.id}.md.bam ${meta.id}.md.bai ${meta.id}.dup_metrics.txt
    """
}
