"""Tests for MULTIQC process outputs."""
import pytest


def test_multiqc_directory_exists(pipeline_results):
    """MULTIQC should publish to results/multiqc/."""
    multiqc_dir = pipeline_results / "multiqc"
    assert multiqc_dir.is_dir(), f"Expected directory {multiqc_dir}"


def test_multiqc_produces_html_report(pipeline_results):
    """MULTIQC should produce multiqc_report.html."""
    multiqc_dir = pipeline_results / "multiqc"
    if not multiqc_dir.is_dir():
        pytest.skip("multiqc dir missing")
    report = multiqc_dir / "multiqc_report.html"
    assert report.is_file(), f"Expected {report}"


def test_multiqc_report_non_empty(pipeline_results):
    """Multiqc report HTML should be non-empty and contain MultiQC content."""
    report = pipeline_results / "multiqc" / "multiqc_report.html"
    if not report.is_file():
        pytest.skip("multiqc_report.html missing")
    text = report.read_text()
    assert len(text) > 100, "Report should be non-trivial"
    assert "multiqc" in text.lower() or "MultiQC" in text, "Expected MultiQC content"
