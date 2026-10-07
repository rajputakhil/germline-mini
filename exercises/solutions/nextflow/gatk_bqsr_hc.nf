// Week 2 exercise solution: BQSR + HaplotypeCaller branch (DeepVariant does NOT need BQSR).
process BQSR {
    tag "${meta.id}"
    container 'broadinstitute/gatk:4.6.1.0'

    input:
    tuple val(meta), path(bam), path(bai)
    path fasta          // needs .fai and .dict alongside
    path known_sites    // e.g. dbSNP + Mills indels VCFs (with .tbi)

    output:
    tuple val(meta), path("${meta.id}.recal.bam"), path("${meta.id}.recal.bai"), emit: bam
    path "${meta.id}.recal.table",                                              emit: table

    script:
    def ks = known_sites.findAll { it.name.endsWith('.vcf.gz') }.collect { "--known-sites ${it}" }.join(' ')
    """
    gatk BaseRecalibrator -R ${fasta} -I ${bam} ${ks} -L ${params.regions} -O ${meta.id}.recal.table
    gatk ApplyBQSR -R ${fasta} -I ${bam} --bqsr-recal-file ${meta.id}.recal.table -O ${meta.id}.recal.bam
    """

    stub:
    """
    touch ${meta.id}.recal.bam ${meta.id}.recal.bai ${meta.id}.recal.table
    """
}

process HAPLOTYPECALLER {
    tag "${meta.id}"
    container 'broadinstitute/gatk:4.6.1.0'
    publishDir "${params.outdir}/vcf", mode: 'copy'

    input:
    tuple val(meta), path(bam), path(bai)
    path fasta

    output:
    tuple val(meta), path("${meta.id}.hc.vcf.gz"), path("${meta.id}.hc.vcf.gz.tbi"), emit: vcf

    script:
    """
    gatk HaplotypeCaller -R ${fasta} -I ${bam} -L ${params.regions} -O ${meta.id}.hc.vcf.gz
    """

    stub:
    """
    touch ${meta.id}.hc.vcf.gz ${meta.id}.hc.vcf.gz.tbi
    """
}
