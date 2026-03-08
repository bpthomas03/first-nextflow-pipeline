/*
 * DSL2 pipeline: FASTQ → FastQC → BWA-MEM → SAMtools sort/index → MultiQC
 * Interview-style bioinformatics pipeline using nf-core test data.
 */

// -------------------------------------------------------------------------
// 1. Parameters (overridable from CLI: -param_name value)
// -------------------------------------------------------------------------
params.reads    = "data/*_R{1,2}.fastq.gz"
params.genome   = "data/ref.fna"
params.outdir   = "results"

// -------------------------------------------------------------------------
// 2. Include process modules (DSL2)
// -------------------------------------------------------------------------
include { FASTQC; BWA_INDEX; BWA_MEM; SAMTOOLS_SORT; MULTIQC } from './modules/main'

// -------------------------------------------------------------------------
// 3. Workflow — wire channels into processes
// -------------------------------------------------------------------------
workflow {
    // Paired-end reads: emits (sample_id, [read1, read2])
    reads_ch = Channel.fromFilePairs(params.reads, checkIfExists: true)

    // Single reference genome
    genome_ch = Channel.fromPath(params.genome, checkIfExists: true)

    // QC on raw reads
    FASTQC(reads_ch)

    // Index reference once, then align each sample and sort/index BAM
    index_ch = BWA_INDEX(genome_ch)
    SAMTOOLS_SORT(BWA_MEM(reads_ch, index_ch))

    // Aggregate all FastQC outputs and run MultiQC
    MULTIQC(FASTQC.out.fastqc_out.collect())
}
