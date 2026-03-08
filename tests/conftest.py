"""
Pytest fixtures for Nextflow pipeline tests.
Runs the pipeline once per session with -profile test and exposes results path.
"""
import shutil
import subprocess
from pathlib import Path

import pytest

# Project root (parent of tests/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "tests" / "results"


def _nextflow_available() -> bool:
    """Check if nextflow is on PATH."""
    return shutil.which("nextflow") is not None


@pytest.fixture(scope="session")
def pipeline_results():
    """
    Run the pipeline with -profile test (output to tests/results).
    Returns the Path to the results directory. Skips all tests if nextflow isn't available.
    """
    if not _nextflow_available():
        pytest.skip("nextflow not found on PATH")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    cmd = [
        "nextflow",
        "run",
        str(PROJECT_ROOT / "main.nf"),
        "-profile", "test",
        "-resume",
        "-work-dir", str(PROJECT_ROOT / "work"),
    ]
    result = subprocess.run(
        cmd,
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        timeout=600,
    )
    if result.returncode != 0:
        pytest.fail(
            f"Pipeline run failed (exit {result.returncode}).\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return RESULTS_DIR
