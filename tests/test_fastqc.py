"""Tests for FASTQC process outputs."""
import pytest


def test_fastqc_directory_exists(pipeline_results):
    """FASTQC should publish output to results/fastqc/."""
    fastqc_dir = pipeline_results / "fastqc"
    assert fastqc_dir.is_dir(), f"Expected directory {fastqc_dir}"


def test_fastqc_produces_per_sample_dirs(pipeline_results):
    """FASTQC should create one directory per sample (e.g. fastqc_SRR11140748)."""
    fastqc_dir = pipeline_results / "fastqc"
    if not fastqc_dir.is_dir():
        pytest.skip("FASTQC output dir missing")
    subdirs = [d for d in fastqc_dir.iterdir() if d.is_dir()]
    assert len(subdirs) >= 1, "Expected at least one sample FastQC output directory"


def test_fastqc_outputs_contain_html_report(pipeline_results):
    """Each FastQC sample dir should contain HTML report(s) or zip."""
    fastqc_dir = pipeline_results / "fastqc"
    if not fastqc_dir.is_dir():
        pytest.skip("FASTQC output dir missing")
    html_or_zip = list(fastqc_dir.rglob("*.html")) + list(fastqc_dir.rglob("*.zip"))
    assert len(html_or_zip) >= 1, "Expected at least one FastQC report (html or zip)"
