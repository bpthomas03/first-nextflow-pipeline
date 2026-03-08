"""Tests for BWA_MEM process outputs (SAM in alignments)."""
import pytest


def test_alignments_directory_exists(pipeline_results):
    """Alignments (BWA_MEM SAM + SAMTOOLS_SORT BAM) go to results/alignments/."""
    align_dir = pipeline_results / "alignments"
    assert align_dir.is_dir(), f"Expected directory {align_dir}"


def test_bwa_mem_produces_sam_files(pipeline_results):
    """BWA_MEM should publish at least one .sam file."""
    align_dir = pipeline_results / "alignments"
    if not align_dir.is_dir():
        pytest.skip("alignments dir missing")
    sam_files = list(align_dir.glob("*.sam"))
    assert len(sam_files) >= 1, "Expected at least one SAM file from BWA_MEM"
