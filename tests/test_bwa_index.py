"""Tests for BWA_INDEX process outputs."""
import pytest


def test_bwa_index_directory_exists(pipeline_results):
    """BWA_INDEX should publish to results/bwa_index/."""
    bwa_dir = pipeline_results / "bwa_index"
    assert bwa_dir.is_dir(), f"Expected directory {bwa_dir}"


def test_bwa_index_produces_index_files(pipeline_results):
    """BWA index creates .amb, .ann, .bwt, .pac, .sa and the reference."""
    bwa_dir = pipeline_results / "bwa_index"
    if not bwa_dir.is_dir():
        pytest.skip("BWA_INDEX output dir missing")
    suffixes = {f.suffix for f in bwa_dir.iterdir() if f.is_file()}
    index_suffixes = {".amb", ".ann", ".bwt", ".pac", ".sa"}
    found = index_suffixes & suffixes
    assert found == index_suffixes, f"Missing BWA index files. Found: {suffixes}"
