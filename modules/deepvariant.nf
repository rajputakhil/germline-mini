process DEEPVARIANT {
    tag "${meta.id}"
    cpus 8
    memory '32 GB'
    container 'google/deepvariant:1.10.0'
    publishDir "${params.outdir}/vcf", mode: 'copy'

    input:
    tuple val(meta), path(bam), path(bai)
    path fasta   // .fai must sit next to the FASTA

    output:
    tuple val(meta), path("${meta.id}.dv.vcf.gz"), path("${meta.id}.dv.vcf.gz.tbi"), emit: vcf

    script:
    """
    /opt/deepvariant/bin/run_deepvariant \\
      --model_type=WES \\
      --ref=${fasta} --reads=${bam} \\
      --regions=${params.regions} \\
      --output_vcf=${meta.id}.dv.vcf.gz \\
      --num_shards=${task.cpus}
    """

    stub:
    """
    touch ${meta.id}.dv.vcf.gz ${meta.id}.dv.vcf.gz.tbi
    """
}
