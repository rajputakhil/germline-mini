process FASTP {
    tag "${meta.id}"
    container 'quay.io/biocontainers/fastp:0.23.4--hadf994f_2'
    publishDir "${params.outdir}/qc", pattern: '*.json', mode: 'copy'

    input:
    tuple val(meta), path(r1), path(r2)

    output:
    tuple val(meta), path("${meta.id}_R{1,2}.trim.fq.gz"), emit: reads
    path "${meta.id}.fastp.json",                          emit: json

    script:
    """
    fastp -i ${r1} -I ${r2} \\
          -o ${meta.id}_R1.trim.fq.gz -O ${meta.id}_R2.trim.fq.gz \\
          --json ${meta.id}.fastp.json --thread ${task.cpus}
    """

    stub:
    """
    touch ${meta.id}_R1.trim.fq.gz ${meta.id}_R2.trim.fq.gz ${meta.id}.fastp.json
    """
}
