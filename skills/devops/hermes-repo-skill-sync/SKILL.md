---
name: hermes-repo-skill-sync
description: >
  Sync skills from a GitHub repository into the local Hermes skills directory.
  Handles flat-to-categorized mapping, umbrella/nested directory dedup,
  collision detection, and framework integration verification.
  Use when the user says "sync repo skills", "pull skills from GitHub",
  "integrate repo into framework", or pushes/updates a skills repo.
triggers:
  - "sync repo"
  - "pull skills from github"
  - "integrate repo into framework"
  - "skills repo update"
  - "hermes skills sync"
---

# Hermes Repo Skill Sync

Sync skills from an external GitHub repository into `~/.hermes/skills/` with proper category mapping.

## When to Use

- User has a GitHub repo of skills (e.g. `mo-Security-Skills`) and wants to sync locally
- After a `git pull` on a skills repo, to propagate updates into Hermes
- After upgrading skills in a repo and wanting them available to the agent

## Prerequisites

- Repo cloned locally (e.g. `/root/mo-Security-Skills/`)
- Repo has `index.json` at root with skill metadata (name, category, path)
- Repo has `skills/<name>/SKILL.md` structure

## Step-by-Step

### 1. Pull Latest

```bash
cd /path/to/repo && git pull
```

### 2. Run Sync Script

See `scripts/sync-repo-skills.py` — handles:
- Reading `index.json` for category mapping
- Falling back to existing local category if skill already exists
- Recursive file sync (only newer files)
- Reporting created/updated/skipped counts

```bash
/usr/bin/python3 ~/.hermes/skills/devops/hermes-repo-skill-sync/scripts/sync-repo-skills.py /path/to/repo
```

### 3. Fix Umbrella Nesting (CRITICAL)

Repo umbrella directories (e.g. `skills/penetration-testing-learning/`) that ARE also skills AND contain sub-skills create nested duplicates:

```
~/.hermes/skills/penetration-testing-learning/penetration-testing-learning/  ← WRONG
```

Detection:
```bash
for cat_dir in ~/.hermes/skills/*/; do
  for skill_dir in "$cat_dir"*/; do
    nested="$skill_dir$(basename "$skill_dir")"
    [ -d "$nested" ] && echo "NESTED: $nested"
  done
done
```

Fix: `rm -rf` the nested directory. Sub-skills already exist at the correct level.

### 4. Verify No Collisions

```python
# skill_view with bare name will error if duplicates exist
skill_view(name="burp-suite-setup")  # → "Ambiguous skill name" if collision
```

Fix by removing the nested duplicate, not by renaming.

### 5. Verify Framework Visibility

```python
skills_list()  # Check total count matches expectations
skills_list(category="target-category")  # Check category-specific skills
```

## Pitfalls

### PITFALL: `cp -ruv` Creates Nested Dirs
When target directory already exists, `cp -ruv src/ dst/` creates `dst/src/` instead of merging.
**Fix**: Use the sync script (which copies file-by-file) or `rsync -av`.

### PITFALL: Umbrella Skill Nesting
Repo `skills/category-name/` containing sub-skills gets synced as BOTH:
- `~/.hermes/skills/category-name/SKILL.md` (umbrella skill itself)
- `~/.hermes/skills/category-name/category-name/` (nested duplicate of children)

The nested copy causes skill name collisions. Always check and clean after sync.

### PITFALL: Shallow Clone + Pull
`git clone --depth 1` works for initial clone. Subsequent `git pull` may fail with
"GnuTLS recv error" on large repos. Use `git fetch --depth 1 origin main && git reset --hard origin/main` as fallback.

### PITFALL: index.json Category Gaps
Some skills in `index.json` may lack a `category` field. The sync script falls back to
the existing local category, then to a hardcoded default. Review the script output for
skills placed in unexpected categories.

### PITFALL: Archived Skills
Skills in `.archive/` locally won't be overwritten by the sync script if their repo
version hasn't changed. If you want to un-archive, move them out of `.archive/` first.
