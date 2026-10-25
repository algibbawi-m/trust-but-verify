"""Make every helper file from the role texts in roles/.

Run: python3 scripts/build.py

roles/<name>.md is the only place a helper is written. This script makes:
  agents/<name>.md                          Claude Code helper (ships in the plugin)
  codex-agents/trust_but_verify_<name>.toml      Codex helper (copied to ~/.codex/agents/)
  skills/<skill>/references/roles/<name>.md fallback text, used when no helper is installed
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MADE_DIRS = ["agents", "codex-agents", "skills/how-we-build/references/roles",
             "skills/design-pass/references/roles"]
READ_ONLY_LINE = "Do not create, edit or delete files."


def made_note(name):
    return f"Made by scripts/build.py from roles/{name}.md. Edit that file instead."


def parse_role(path):
    text = path.read_text()
    _, head, body = text.split("---\n", 2)
    meta = {}
    for line in head.strip().splitlines():
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    meta["read_only"] = meta.get("read_only") == "true"
    meta["skills"] = [s.strip() for s in meta["skills"].split(",")]
    if meta["name"] != path.stem:
        sys.exit(f"{path}: name '{meta['name']}' must match the file name '{path.stem}'")
    return meta, body.strip() + "\n"


def claude_agent(meta, body):
    lines = ["---", f"name: {meta['name']}", f"description: {meta['description']}",
             f"effort: {meta['effort']}"]
    if meta["read_only"]:
        lines.append("disallowedTools: Edit, Write, NotebookEdit")
    lines += ["---", f"<!-- {made_note(meta['name'])} -->", "", body]
    return "\n".join(lines)


def codex_agent(meta, body):
    instructions = (READ_ONLY_LINE + "\n\n" + body) if meta["read_only"] else body
    if "'''" in instructions:
        sys.exit(f"roles/{meta['name']}.md: the text may not contain three single quotes")
    return "\n".join([
        f"# {made_note(meta['name'])}",
        f"name = {json.dumps(codex_name(meta['name']))}",
        f"description = {json.dumps(meta['description'], ensure_ascii=False)}",
        f"model_reasoning_effort = {json.dumps(meta['effort'])}",
        f"developer_instructions = '''\n{instructions}'''",
        "",
    ])


def codex_name(name):
    return "trust_but_verify_" + name.replace("-", "_")


def fallback_role(meta, body):
    lines = [f"<!-- {made_note(meta['name'])} -->", f"# Helper role: {meta['name']}", "",
             f"Use this text when the kit's `{meta['name']}` helper is not installed. Start a "
             "fresh helper (a subagent) with this text, then the task.", ""]
    if meta["read_only"]:
        lines += [READ_ONLY_LINE, ""]
    return "\n".join(lines) + body


def render(root=ROOT):
    """Return {relative path: content} for every made file."""
    out = {}
    for path in sorted((root / "roles").glob("*.md")):
        meta, body = parse_role(path)
        name = meta["name"]
        out[f"agents/{name}.md"] = claude_agent(meta, body)
        out[f"codex-agents/{codex_name(name)}.toml"] = codex_agent(meta, body)
        for skill in meta["skills"]:
            out[f"skills/{skill}/references/roles/{name}.md"] = fallback_role(meta, body)
    return out


def made_files_on_disk(root=ROOT):
    found = set()
    for folder in MADE_DIRS:
        base = root / folder
        if base.is_dir():
            found |= {str(p.relative_to(root)) for p in base.iterdir() if p.is_file()}
    return found


def main():
    files = render()
    for rel in made_files_on_disk() - set(files):
        (ROOT / rel).unlink()
        print(f"removed {rel}")
    for rel, content in files.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    print(f"made {len(files)} files from roles/")


if __name__ == "__main__":
    main()
