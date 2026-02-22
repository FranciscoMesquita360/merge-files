#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTS FOR merge_files.py
================================================================================
Usage:
  python test_merge_files.py
  python test_merge_files.py -v    # verbose (show each subtest)
================================================================================
Requirements:
  - merge_files.py must be in the same directory as this test file.
================================================================================
"""

import os
import sys
import shutil
import tempfile
import argparse
import subprocess

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "merge_files.py")

# ═══════════════════════════════════════════════════════════════════════════
# 🏗️  FIXTURES
# ═══════════════════════════════════════════════════════════════════════════

SAMPLE_FILES = {
    "src/utils/helpers.py": (
        "# src/utils/helpers.py\n"
        "def add(a, b):\n"
        "    return a + b\n"
        "\n"
        "def greet(name):\n"
        "    return f\"Hello, {name}!\"\n"
    ),
    "src/api/routes.ts": (
        "// src/api/routes.ts\n"
        "export const BASE_URL = \"https://api.example.com\";\n"
        "\n"
        "export function getRoute(path: string): string {\n"
        "    return `${BASE_URL}/${path}`;\n"
        "}\n"
    ),
    "config/settings.toml": (
        "# config/settings.toml\n"
        "[database]\n"
        "host = \"localhost\"\n"
        "port = 5432\n"
        "password = \"supersecret123\"\n"
    ),
    "src/api/auth.py": (
        "# src/api/auth.py\n"
        "api_key = \"sk-abc123verylongapikey987654321abcdefghijklmno\"\n"
        "token = \"mytoken_abc123\"\n"
        "\n"
        "def authenticate(user, pwd):\n"
        "    password = \"hardcoded_pass\"\n"
        "    return True\n"
    ),
}

# Files that should survive a round-trip identical (no secrets → not sanitized)
CLEAN_FILES = ["src/utils/helpers.py", "src/api/routes.ts"]


def build_project(base_dir):
    """Create the sample project tree under base_dir."""
    for rel_path, content in SAMPLE_FILES.items():
        full = os.path.join(base_dir, rel_path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)


def run(args, cwd=None):
    """Run merge_files.py with given args list. Returns (returncode, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, SCRIPT] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


# ═══════════════════════════════════════════════════════════════════════════
# 🧪 TEST RUNNER
# ═══════════════════════════════════════════════════════════════════════════

class TestRunner:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.results = []

    def check(self, name, condition, detail=""):
        passed = bool(condition)
        self.results.append((name, passed, detail))
        icon = "✅" if passed else "❌"
        if self.verbose or not passed:
            detail_str = f"  → {detail}" if detail else ""
            print(f"  {icon} {name}{detail_str}")
        return passed

    def summary(self):
        total  = len(self.results)
        passed = sum(1 for _, p, _ in self.results)
        failed = total - passed
        print()
        print("─" * 60)
        print(f"  {'✅' if failed == 0 else '❌'} {passed}/{total} tests passed", end="")
        if failed:
            print(f"  ({failed} FAILED)")
            print()
            for name, ok, detail in self.results:
                if not ok:
                    print(f"     ❌ {name}")
                    if detail:
                        print(f"        {detail}")
        else:
            print()
        print("─" * 60)
        return failed == 0


# ═══════════════════════════════════════════════════════════════════════════
# 🔬 TESTS
# ═══════════════════════════════════════════════════════════════════════════

def run_tests(verbose=False):
    t = TestRunner(verbose=verbose)
    base = tempfile.mkdtemp(prefix="merge_test_")

    try:
        project_dir = os.path.join(base, "myproject")
        os.makedirs(project_dir)
        build_project(project_dir)

        merged_file = os.path.join(project_dir, "merged_output_myproject.md")

        # ── MERGE ────────────────────────────────────────────────────────
        print("\n🔗 MERGE TESTS")
        print("─" * 60)

        rc, out, err = run([], cwd=project_dir)
        t.check("merge: exits with code 0", rc == 0, err.strip() if err else "")
        t.check("merge: output file created", os.path.exists(merged_file))
        t.check("merge: output file non-empty", os.path.getsize(merged_file) > 0)

        if os.path.exists(merged_file):
            content = open(merged_file, encoding="utf-8").read()
            t.check("merge: contains directory tree section", "# PROJECT DIRECTORY TREE" in content)
            t.check("merge: contains file sections",          "## File:" in content)
            t.check("merge: all 4 files listed",              content.count("## File:") == 4)
            t.check("merge: sanitization notice present",     "SECURITY NOTICE" in content)
            t.check("merge: secrets redacted in toml",        "supersecret123" not in content)
            t.check("merge: secrets redacted in auth.py",     "sk-abc123" not in content)
            t.check("merge: clean files untouched (helpers)", "def add(a, b)" in content)
            t.check("merge: clean files untouched (routes)",  "BASE_URL" in content)

        # ── UNMERGE — fresh directory ────────────────────────────────────
        print("\n🔓 UNMERGE TESTS")
        print("─" * 60)

        restore1 = os.path.join(base, "restore1")
        os.makedirs(restore1)

        rc, out, err = run(["unmerge", merged_file, "-o", restore1])
        t.check("unmerge: exits with code 0",    rc == 0, err.strip() if err else "")
        t.check("unmerge: written=4 in summary", "Written         : 4" in out)
        t.check("unmerge: skipped=0 in summary", "Skipped         : 0" in out)

        for rel in SAMPLE_FILES:
            t.check(f"unmerge: file exists — {rel}", os.path.exists(os.path.join(restore1, rel)))

        # Content integrity for clean (non-sanitized) files
        for rel in CLEAN_FILES:
            orig    = SAMPLE_FILES[rel]
            restored = open(os.path.join(restore1, rel), encoding="utf-8").read()
            t.check(f"unmerge: content identical — {rel}", orig == restored,
                    f"len orig={len(orig)} restored={len(restored)}")

        # ── UNMERGE — skip existing (default) ───────────────────────────
        print("\n⏭️  SKIP EXISTING TESTS")
        print("─" * 60)

        rc, out, err = run(["unmerge", merged_file, "-o", restore1])
        t.check("skip: exits with code 0",       rc == 0)
        t.check("skip: skipped=4 in summary",    "Skipped         : 4" in out)
        t.check("skip: written=0 in summary",    "Written         : 0" in out)

        # ── UNMERGE — overwrite ──────────────────────────────────────────
        print("\n♻️  OVERWRITE TESTS")
        print("─" * 60)

        # Corrupt a file first
        victim = os.path.join(restore1, "src/utils/helpers.py")
        with open(victim, "w") as f:
            f.write("CORRUPTED\n")

        rc, out, err = run(["unmerge", merged_file, "-o", restore1, "--overwrite"])
        t.check("overwrite: exits with code 0",        rc == 0)
        t.check("overwrite: overwritten=4 in summary", "Overwritten     : 4" in out)
        restored = open(victim, encoding="utf-8").read()
        t.check("overwrite: corrupted file restored",  "CORRUPTED" not in restored)
        t.check("overwrite: content correct after",    SAMPLE_FILES["src/utils/helpers.py"] == restored)

        # ── DRY RUN ──────────────────────────────────────────────────────
        print("\n🔍 DRY RUN TESTS")
        print("─" * 60)

        dry_dir = os.path.join(base, "dry_dir")
        os.makedirs(dry_dir)

        rc, out, err = run(["unmerge", merged_file, "-o", dry_dir, "--dry-run"])
        t.check("dry-run: exits with code 0",     rc == 0)
        t.check("dry-run: no files written",      len(os.listdir(dry_dir)) == 0)
        t.check("dry-run: DRY RUN label in out",  "DRY RUN" in out)

        # Dry-run with overwrite on existing dir
        rc, out, err = run(["unmerge", merged_file, "-o", restore1, "--dry-run", "--overwrite"])
        t.check("dry-run+overwrite: shows OVERWRITE actions", "OVERWRITE" in out)
        t.check("dry-run+overwrite: no files actually changed",
                open(os.path.join(restore1, "src/api/routes.ts"), encoding="utf-8").read() != "")

        # ── VERBOSE ──────────────────────────────────────────────────────
        print("\n💬 VERBOSE TESTS")
        print("─" * 60)

        restore2 = os.path.join(base, "restore2")
        os.makedirs(restore2)

        rc, out, err = run(["unmerge", merged_file, "-o", restore2, "-v"])
        t.check("verbose: WRITE lines shown", "WRITE" in out)

        rc, out, err = run(["unmerge", merged_file, "-o", restore2, "-v"])
        t.check("verbose: SKIP lines shown",  "SKIP" in out)

        # ── ERROR HANDLING ───────────────────────────────────────────────
        print("\n⚠️  ERROR HANDLING TESTS")
        print("─" * 60)

        rc, out, err = run(["unmerge", "/nonexistent/path/file.md"])
        t.check("missing input: exits with code 1", rc == 1)
        t.check("missing input: error message shown", "File not found" in out or "not found" in out.lower())

        # ── GENERATE CONFIG ──────────────────────────────────────────────
        print("\n⚙️  CONFIG GENERATION TEST")
        print("─" * 60)

        cfg_dir = os.path.join(base, "cfg_test")
        os.makedirs(cfg_dir)
        rc, out, err = run(["-g"], cwd=cfg_dir)
        t.check("generate-config: exits with code 0",       rc == 0)
        t.check("generate-config: merge_config.json created",
                os.path.exists(os.path.join(cfg_dir, "merge_config.json")))

    finally:
        shutil.rmtree(base, ignore_errors=True)

    return t.summary()


# ═══════════════════════════════════════════════════════════════════════════
# 🚀 ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🧪 Tests for merge_files.py")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Show every individual test result")
    args = parser.parse_args()

    if not os.path.exists(SCRIPT):
        print(f"❌ merge_files.py not found at: {SCRIPT}")
        print("   Place this test file in the same directory as merge_files.py")
        sys.exit(1)

    print("=" * 60)
    print("🧪 merge_files.py — TEST SUITE")
    print("=" * 60)

    ok = run_tests(verbose=args.verbose)
    sys.exit(0 if ok else 1)