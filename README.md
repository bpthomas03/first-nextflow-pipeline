# hello-nextflow

DSL2 pipeline: **FASTQ → FastQC → BWA-MEM → SAMtools sort/index → MultiQC**

Uses [nf-core/test-datasets](https://github.com/nf-core/test-datasets) (viralrecon branch) for small test data.

## Requirements

- Nextflow (Java 11+)
- Docker (or enable Singularity in `nextflow.config` for HPC)

**WSL2:** Ensure Docker Desktop has WSL integration enabled (Settings → Resources → WSL Integration → turn on your Ubuntu distro) so `docker` is available inside Ubuntu.

## Data

Test data is under `data/`:

- **Reads:** `data/*_R{1,2}.fastq.gz` (two samples: SRR11140748, SRR11140750)
- **Reference:** `data/ref.fna` (SARS-CoV-2 subset from nf-core test-datasets)

## Run

```bash
cd /home/bpthomas/hello-nextflow   # or your project path

# With Docker (default in nextflow.config)
nextflow run main.nf

# Override params
nextflow run main.nf --reads "data/*_R{1,2}.fastq.gz" --genome data/ref.fna --outdir results

# Resume after a failure
nextflow run main.nf -resume
```

Outputs go to `results/` (or `--outdir`): `fastqc/`, `alignments/`, `multiqc/`.

## Tests

Unit/integration tests (per-process output checks + workflow dry-run) use pytest. The test run executes the pipeline once with `-profile test` (output to `tests/results/`), then asserts on each process’s outputs.

```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows Git Bash: .venv/Scripts/activate
pip install -r requirements-test.txt
pytest tests/ -v
```

Quick check (no pipeline run, only file structure + `nextflow inspect`):

```bash
pytest tests/test_workflow.py -v
```

- **Workflow:** `test_workflow.py` — checks `main.nf`/`modules/main.nf`/config exist and `nextflow inspect main.nf` succeeds.
- **Processes:** `test_fastqc.py`, `test_bwa_index.py`, `test_bwa_mem.py`, `test_samtools_sort.py`, `test_multiqc.py` — assert expected files/dirs exist after a run.

Requires Nextflow and Docker (or Singularity) for the full test run; workflow-only tests (`pytest tests/test_workflow.py`) skip if `nextflow` is not on PATH.

## Structure

- `main.nf` — params, includes, workflow
- `nextflow.config` — Docker, publishDir
- `modules/main.nf` — processes: FASTQC, BWA_INDEX, BWA_MEM, SAMTOOLS_SORT, MULTIQC

## Concepts (for interview)

- **Channels:** `fromFilePairs` for paired reads, `fromPath` for reference; processes consume from channels asynchronously.
- **Processes:** Input/output declarations; `container` for reproducibility; `publishDir` in config.
- **DSL2:** Single `include` of modules; workflow wires channels to processes; `collect()` for MultiQC aggregation.
