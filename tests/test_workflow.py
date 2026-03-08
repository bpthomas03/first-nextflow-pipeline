"""Tests for workflow structure and validation (no execution)."""
import shutil
import subprocess
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_main_nf_exists():
    """Pipeline entry point main.nf must exist."""
    assert (PROJECT_ROOT / "main.nf").is_file()


def test_modules_main_nf_exists():
    """Process definitions module must exist."""
    assert (PROJECT_ROOT / "modules" / "main.nf").is_file()


def test_nextflow_config_exists():
    """nextflow.config must exist."""
    assert (PROJECT_ROOT / "nextflow.config").is_file()


def test_nextflow_inspect_validates():
    """
    nextflow inspect validates the pipeline script loads and reports process info.
    Skips if nextflow not on PATH.
    """
    if shutil.which("nextflow") is None:
        pytest.skip("nextflow not on PATH")
    result = subprocess.run(
        ["nextflow", "inspect", str(PROJECT_ROOT / "main.nf")],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, (
        f"nextflow inspect failed.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    # Should list our processes
    out = result.stdout + result.stderr
    assert "FASTQC" in out or "fastqc" in out.lower(), "Expected pipeline to expose process info"
