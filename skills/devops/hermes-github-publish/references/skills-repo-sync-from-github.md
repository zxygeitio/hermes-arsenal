# Sync Skills FROM a GitHub Skill Repo into Local Hermes

## When to Use

- User says "sync my skills repo" / "pull latest skills" / "import from GitHub"
- User has a GitHub skill repo (agentskills.io format) and wants to update local `~/.hermes/skills/`
- Inverse of the publish workflow — consuming rather than producing

## Workflow

### Step 1: Clone the Repo

```bash
# Full clone (preferred, preserves history)
cd /root && git clone https://github.com/OWNER/REPO.git

# Shallow clone when full clone times out (GnuTLS recv error, large repos)
cd /root && rm -rf REPO && git clone --depth 1 https://github.com/OWNER/REPO.git
```

**Pitfall**: Large repos or slow connections cause `GnuTLS recv error (-9)` / `unexpected disconnect`. Switch to `--depth 1` immediately — don't retry the full clone.

### Step 2: Map Categories via index.json

The repo's `index.json` contains `category` per skill. Build a name→category map:

```python
import json
with open("REPO/index.json") as f:
    data = json.load(f)
name_to_cat = {s["name"]: s.get("category", "") for s in data["skills"]}
```

### Step 3: Three-Tier Category Resolution

For each skill in the repo, determine the target local directory:

1. **index.json category** (authoritative) — e.g. `"ai-development"`
2. **Existing local category** (fallback) — check `~/.hermes/skills/*/<skill-name>/SKILL.md`
3. **Default** — `penetration-testing-learning` for security skills

```python
import os
LOCAL = os.path.expanduser("~/.hermes/skills")

# Build reverse map from existing local skills
existing_local = {}
for cat_dir in os.listdir(LOCAL):
    cat_path = os.path.join(LOCAL, cat_dir)
    if os.path.isdir(cat_path):
        for skill_name in os.listdir(cat_path):
            if os.path.isdir(os.path.join(cat_path, skill_name)):
                existing_local[skill_name] = cat_dir

# Resolve category for each repo skill
for skill_name in os.listdir("REPO/skills/"):
    if skill_name in name_to_cat and name_to_cat[skill_name]:
        cat = name_to_cat[skill_name]
    elif skill_name in existing_local:
        cat = existing_local[skill_name]
    else:
        cat = "penetration-testing-learning"
```

### Step 4: mtime-Based Skip + Copy

Compare `SKILL.md` modification times to avoid unnecessary overwrites:

```python
import shutil

for skill_name, cat in resolved_skills.items():
    src = f"REPO/skills/{skill_name}"
    dst = os.path.join(LOCAL, cat, skill_name)
    os.makedirs(os.path.join(LOCAL, cat), exist_ok=True)
    
    if os.path.exists(dst):
        repo_md = os.path.join(src, "SKILL.md")
        local_md = os.path.join(dst, "SKILL.md")
        if os.path.exists(repo_md) and os.path.exists(local_md):
            if os.path.getmtime(repo_md) <= os.path.getmtime(local_md):
                continue  # Local is same or newer
        shutil.rmtree(dst)
    
    shutil.copytree(src, dst)
```

### Step 5: Verify

```bash
# Check no repo skills were missed
comm -23 <(ls REPO/skills/) <(find ~/.hermes/skills -mindepth 2 -maxdepth 2 -type d -exec basename {} \; | sort -u)
```

## Pitfalls

1. **Shallow clone for reliability** — `git clone --depth 1` is faster and avoids TLS errors. History isn't needed for sync.

2. **python3 vs python** — On Kali, `python3` may not be in PATH. Use `/usr/bin/python3` explicitly in scripts.

3. **.archive/ directory** — Some skills may already be in `~/.hermes/skills/.archive/` from prior cleanup. The sync script should handle these gracefully (they won't appear in the `find` results but may exist).

4. **index.json may not cover all skills** — Some skills in the repo may lack a `category` field. The three-tier resolution handles this by falling back to existing local placement or a sensible default.

5. **Skills without SKILL.md** — Directories in `skills/` that are subdirectories (like `references/`) or lack `SKILL.md` should be skipped. Check `os.path.isdir()` + existence of `SKILL.md`.

6. **Don't overwrite local-only modifications** — The mtime check prevents this, but if you've patched a local skill and the repo version is older, the local version is preserved.
