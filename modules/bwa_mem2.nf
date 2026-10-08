process BWA_MEM2 {
    tag "${meta.id}"
    cpus 8
    memory '16 GB'
    // needs bwa-mem2 + samtools; build a small image or use a mulled biocontainer
    container 'germline-mini/bwa-mem2-samtools:2.2.1'

    input:
    tuple val(meta), path(reads)
    path fasta
    path index      // bwa-mem2 index files, staged next to the FASTA

    output:
    tuple val(meta), path("${meta.id}.sorted.bam"), emit: bam

    script:
    def rg = "@RG\\tID:${meta.id}\\tSM:${meta.id}\\tPL:ILLUMINA"
    """
    bwa-mem2 mem -t ${task.cpus} -R '${rg}' ${fasta} ${reads[0]} ${reads[1]} \\
      | samtools sort -@ ${task.cpus} -o ${meta.id}.sorted.bam -
    """

    stub:
    """
    touch ${meta.id}.sorted.bam
    """
}
