import subprocess
from pathlib import Path
import json

REPO_ROOT = Path(__file__).resolve().parents[3]
KB_SOURCES = REPO_ROOT / "knowledge" / "sources"
NORMALIZED = REPO_ROOT / "knowledge" / "normalized"
INDEX = REPO_ROOT / "knowledge" / "index" / "index.json"


def test_ingest_and_build_index(tmp_path):
    # prepare sample HTML source
    KB_SOURCES.mkdir(parents=True, exist_ok=True)
    sample = KB_SOURCES / "sample_test_page.html"
    sample.write_text("<html><body><h1>睡眠建議</h1><p>規律作息。</p></body></html>", encoding="utf8")

    # run ingest script
    res = subprocess.run(
        ["python", "scripts/ingest.py", "--source", str(sample)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, (
        f"ingest.py failed with returncode {res.returncode}\n"
        f"stdout:\n{res.stdout}\n"
        f"stderr:\n{res.stderr}\n"
    )

    # verify normalized fragment exists
    norm_dir = NORMALIZED / "sample_test_page"
    assert norm_dir.exists()
    md = norm_dir / "00_raw.md"
    assert md.exists()
    content = md.read_text(encoding="utf8")
    assert "睡眠建議" in content or "sample_test_page.html" in content

    # run build_index
    res2 = subprocess.run(
        ["python", "scripts/build_index.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert res2.returncode == 0, (
        f"build_index.py failed with returncode {res2.returncode}\n"
        f"stdout:\n{res2.stdout}\n"
        f"stderr:\n{res2.stderr}\n"
    )

    # index file exists and contains our sample entry
    assert INDEX.exists()
    idx = json.loads(INDEX.read_text(encoding="utf8"))
    assert any("sample_test_page" in e.get("id", "") or "sample_test_page" in e.get("source", "") for e in idx)
