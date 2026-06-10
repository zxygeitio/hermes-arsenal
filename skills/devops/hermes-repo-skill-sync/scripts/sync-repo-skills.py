#!/usr/bin/env python3
"""Sync skills from a GitHub repo into ~/.hermes/skills/ with category mapping.

Usage: /usr/bin/python3 sync-repo-skills.py /path/to/repo

Requires: repo has index.json with skill metadata and skills/<name>/SKILL.md structure.
"""
import json, os, shutil, sys

def load_index(repo_path):
    index_path = os.path.join(repo_path, "index.json")
    with open(index_path) as f:
        data = json.load(f)
    name_to_cat = {}
    for s in data.get("skills", []):
        cat = s.get("category", "")
        if cat:
            name_to_cat[s["name"]] = cat
    return name_to_cat

def build_existing_local(local_skills):
    """Map existing skill names to their current local category."""
    existing = {}
    for cat_dir in os.listdir(local_skills):
        cat_path = os.path.join(local_skills, cat_dir)
        if not os.path.isdir(cat_path) or cat_dir.startswith("."):
            continue
        for skill_name in os.listdir(cat_path):
            skill_path = os.path.join(cat_path, skill_name)
            if os.path.isdir(skill_path) and os.path.exists(os.path.join(skill_path, "SKILL.md")):
                existing[skill_name] = cat_dir
    return existing

def sync_tree(src, dst):
    """Sync src into dst, only overwriting newer files. Returns True if changed."""
    os.makedirs(dst, exist_ok=True)
    changed = False
    for item in os.listdir(src):
        s, d = os.path.join(src, item), os.path.join(dst, item)
        if os.path.isdir(s):
            if sync_tree(s, d):
                changed = True
        else:
            if not os.path.exists(d) or os.path.getmtime(s) > os.path.getmtime(d):
                shutil.copy2(s, d)
                changed = True
    return changed

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} /path/to/repo [local_skills_dir]")
        sys.exit(1)

    repo_path = sys.argv[1]
    local_skills = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/.hermes/skills")
    repo_skills = os.path.join(repo_path, "skills")

    if not os.path.exists(os.path.join(repo_path, "index.json")):
        print(f"ERROR: No index.json found in {repo_path}")
        sys.exit(1)

    name_to_cat = load_index(repo_path)
    existing_local = build_existing_local(local_skills)

    default_cat = "penetration-testing-learning"
    updated = created = skipped = 0

    for skill_name in sorted(os.listdir(repo_skills)):
        src = os.path.join(repo_skills, skill_name)
        if not os.path.isdir(src):
            continue

        cat = name_to_cat.get(skill_name) or existing_local.get(skill_name) or default_cat
        target = os.path.join(local_skills, cat, skill_name)

        if sync_tree(src, target):
            if os.path.exists(os.path.join(target, "SKILL.md")):
                action = "UPDATED" if skill_name in existing_local else "CREATED"
                print(f"  {action}: {cat}/{skill_name}")
                if action == "CREATED":
                    created += 1
                else:
                    updated += 1
        else:
            skipped += 1

    # Fix umbrella nesting
    for cat_dir in os.listdir(local_skills):
        cat_path = os.path.join(local_skills, cat_dir)
        if not os.path.isdir(cat_path):
            continue
        for skill_name in os.listdir(cat_path):
            nested = os.path.join(cat_path, skill_name, skill_name)
            if os.path.isdir(nested):
                shutil.rmtree(nested)
                print(f"  FIXED NESTING: {cat_dir}/{skill_name}/{skill_name}")

    print(f"\nSync complete: {updated} updated, {created} created, {skipped} unchanged")

if __name__ == "__main__":
    main()
