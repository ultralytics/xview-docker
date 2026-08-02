# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, etc.) when working with code in this repository. CLAUDE.md is a symlink to this file.

Ultralytics `xview-docker` (AGPL-3.0) packages a trained YOLOv3 detector into a Docker container for submission to the [xView Detection Challenge](https://challenge.xviewdataset.org/). It is the inference-only companion to [`ultralytics/xview-yolov3`](https://github.com/ultralytics/xview-yolov3): the model code is a trimmed copy of that repo, and the container's only job is to run `run.sh <image.tif> <output_dir>` and write one prediction text file.

## Core Principles (CRITICAL)

**Less is more. The simplest solution is the best solution.** The action hierarchy for every change: **Delete > Replace > Add**.

1. **Solve at the owner**: Put behavior in the code path that owns or observes it. For fixes, never guard a symptom with a staleness check, initialization flag, skip-first-call branch, or `try/except` around broken logic; relocate the trigger and delete the wrong path. For features, extend the existing owner rather than creating a parallel abstraction.
2. **Search and reuse first**: Search the whole repository before creating a feature, component, helper, workflow, or utility. Reuse or adapt what exists, consolidate in-scope duplication in the shared owner, and delete duplicate paths. Three similar lines beat a helper nobody else calls.
3. **Delete and modify existing code before creating new code**: Bugfixes are net-negative by default unless deletion and relocation are demonstrably impossible. A new file must first prove it cannot fit cleanly in an existing owner.
4. **Keep scope minimal**: Implement only the simplest complete solution. Avoid impossible-state handling, speculative flags, compatibility shims, policy scaffolding, and unrelated cleanup. Tests are out of scope by default — rely on existing coverage and focused validation; only an uncovered, high-risk regression path justifies minimal new test code.
5. **Ship zero-regression, production-ready changes**: Understand what you remove instead of retaining broken code as insurance. Remove unused imports, functions, types, files, and comments; run relevant cleanup checks; and thoroughly debug and validate the changed owner. Do not break existing features or workflows unless the PR intentionally removes them with evidence.

**Review gate:** for every addition, the reviewer decides whether deleting or changing existing code would have fixed the problem instead — if it would, that is a blocking finding. A missing or thin PR description is never itself a finding.

NEVER push to `main`. NEVER force push. Always start work in a new git worktree (`git worktree add`) on a feature branch and open a PR — never edit the primary checkout directly, it may hold in-flight work.

## PR Workflow

After opening a PR:

1. Wait for the automated PR review and auto-format commit from Ultralytics Actions (`format.yml`), then pull and address every finding.
2. Review the full diff in-session against the Core Principles, performance, and the review gate above, then batch the fixes into one commit and push. After each round of bot or human commits, pull and resume the same reviewer on `<last-reviewed-sha>..HEAD` plus anything that delta could have invalidated. Repeat until the local head matches the live head.
3. Hand off or merge only on a clean final pass: one cold full-diff review returning LGTM with no findings, on a head that is still live at merge time.
4. Never fight other commits: Ultralytics Actions pushes auto-format and header commits, and multiple users may work on the same PR. `git pull --rebase` before pushing; never reset or revert commits you did not author.
5. After the PR merges, clean up: remove local worktrees and branches for it, then `git checkout main && git pull`.

## Commands

```bash
pip3 install -U -r requirements.txt                       # local install
mkdir checkpoints && cp ../xview-yolov3/weights/best.pt checkpoints/   # detect.py expects checkpoints/best.pt
bash run.sh ./1047.tif ./tmp                              # run inference locally on the bundled sample chip
chmod +x run.sh && sudo docker build -t friendlyhello .   # chmod BEFORE build; the bit is baked into the image
sudo docker tag friendlyhello ultralytics/xview:v30
sudo docker run -it --memory=8g --cpus=1 ultralytics/xview:v30 bash -c './run.sh /1047.tif /tmp && cat /tmp/1047.tif.txt'
```

- There is no test suite, no `pyproject.toml`, and no Python packaging. CI is limited to `format.yml` (Ultralytics Actions) and `cla.yml` — nothing builds or runs the container on PRs.
- `checkpoints/` is gitignored and no weights ship in the repo, so `detect.py` cannot run on a fresh clone until a checkpoint is copied in.

## Architecture

- `run.sh` — the container entry point the challenge harness calls; it is a single `python3 detect.py -image_folder $1 -output_folder $2` line wrapped in historical setup notes.
- `detect.py` — loads `checkpoints/best.pt` (and optionally `checkpoints/classifier.pt` under `-secondary_classifier`), tiles the input GeoTIFF, runs the `Darknet` model from `models.py`, and writes `<output_folder>/<image>.txt` predictions plus an annotated JPEG into `<output_folder>_img/`. Flags use a single dash (`-image_folder`, `-cfg`, `-conf_thres`), not `--`.
- `models.py`, `utils/` — a trimmed copy of the `xview-yolov3` model and helper code, built from the Darknet `cfg/*.cfg` files rather than YAMLs. Fix bugs in `xview-yolov3` first; this copy exists only to keep the container self-contained.
- `Dockerfile` — pinned to `python:3.6.5-onbuild`, and `requirements.txt` pins the matching cp36 PyTorch 0.4.1 CPU wheel. These pins are what the submitted challenge container was built with; changing either changes the artifact, so treat them as frozen unless the task is explicitly to rebuild.

## Conventions

- Every Python file and shell script carries the `# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license` header (after the shebang in scripts) — Ultralytics Actions adds these automatically; don't add or revert them manually.
- Google-style docstrings; the Actions bot runs Ruff, docformatter, prettier (YAML/JSON/Markdown), and codespell on PRs and its output can differ from a bare local run — expect bot commits on the branch and `git pull --rebase` before pushing again.
- No version string and no release process: the deliverable is a Docker Hub tag on [`ultralytics/xview`](https://hub.docker.com/r/ultralytics/xview), not a package.
