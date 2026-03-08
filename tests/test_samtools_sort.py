"""Tests for SAMTOOLS_SORT process outputs (BAM + BAI)."""
import pytest


def test_samtools_sort_produces_bam_files(pipeline_results):
    """SAMTOOLS_SORT should produce .bam files in alignments/."""
    align_dir = pipeline_results / "alignments"
    if not align_dir.is_dir():
        pytest.skip("alignments dir missing")
    bam_files = list(align_dir.glob("*.bam"))
    assert len(bam_files) >= 1, "Expected at least one BAM file from SAMTOOLS_SORT"


def test_samtools_sort_produces_bai_index(pipeline_results):
    """Each BAM should have a corresponding .bam.bai index."""
    align_dir = pipeline_results / "alignments"
    if not align_dir.is_dir():
        pytest.skip("alignments dir missing")
    bam_files = list(align_dir.glob("*.bam"))
    for bam in bam_files:
        bai = align_dir / f"{bam.name}.bai"
        assert bai.exists(), f"Missing index {bai} for {bam}"
