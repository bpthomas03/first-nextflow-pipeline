/*
 * Process definitions: FastQC, BWA index, BWA-MEM + SAMtools, MultiQC
 */

// -------------------------------------------------------------------------
// FastQC — quality control on paired-end FASTQ
// -------------------------------------------------------------------------
process FASTQC {
    label 'low'
    container 'biocontainers/fastqc:v0.11.9_cv8'

    input:
    tuple val(sample_id), path(reads)

    output:
    path "fastqc_*", emit: fastqc_out

    script:
    def prefix = file(sample_id).getName()
    """
    mkdir -p fastqc_${prefix}
    fastqc ${reads} --outdir fastqc_${prefix} --extract
    """
}

// -------------------------------------------------------------------------
// BWA index — build index for the reference genome
// -------------------------------------------------------------------------
process BWA_INDEX {
    label 'low'
    container 'biocontainers/bwa:v0.7.17_cv1'

    input:
    path genome

    output:
    tuple path(genome), path("*.{amb,ann,bwt,pac,sa}"), emit: index

    script:
    """
    bwa index ${genome}
    """
}

// -------------------------------------------------------------------------
// BWA-MEM — align reads to reference, output SAM
// -------------------------------------------------------------------------
process BWA_MEM {
    label 'low'
    container 'biocontainers/bwa:v0.7.17_cv1'

    input:
    tuple val(sample_id), path(reads)
    tuple path(genome), path(index_files)

    output:
    tuple val(sample_id), path("*.sam"), emit: sam

    script:
    def prefix = file(sample_id).getName()
    def read_args = reads instanceof List ? reads.join(' ') : reads
    """
    bwa mem ${genome} ${read_args} > ${prefix}.sam
    """
}

// -------------------------------------------------------------------------
// SAMTOOLS_SORT — sort SAM to BAM and index
// -------------------------------------------------------------------------
process SAMTOOLS_SORT {
    label 'low'
    container 'biocontainers/samtools:v1.9-4-deb_cv1'

    input:
    tuple val(sample_id), path(sam)

    output:
    tuple val(sample_id), path("*.bam"), path("*.bam.bai"), emit: bam

    script:
    def prefix = file(sample_id).getName()
    """
    samtools sort -o ${prefix}.bam ${sam}
    samtools index ${prefix}.bam
    """
}

// -------------------------------------------------------------------------
// MultiQC — aggregate FastQC (and other) reports
// -------------------------------------------------------------------------
process MULTIQC {
    label 'low'
    container 'multiqc/multiqc:latest'

    input:
    path fastqc_dirs

    output:
    path "multiqc_report.html", emit: report
    path "multiqc*_data", emit: data  // matches multiqc_data or multiqc_report_data

    script:
    """
    multiqc . -o . -n multiqc_report
    """
}
