#!/usr/bin/env python3
"""
token-sisyphus evolve mode — self-improving agent pipeline

Four-agent pipeline:
  1. Architect  — analyzes wish, designs solution
  2. Coder      — produces a unified diff (patch) implementing the changes
  3. Reviewer   — reviews the diff for correctness and safety
  4. Tester     — generates test cases for the new feature

Outputs:
  - burn.py        (patched in place)
  - CHANGES.md     (what changed and why)
  - Opens a GitHub PR automatically if all agents pass

Usage:
  python evolve.py --wish "add email summary after each run" --target 30k
  python evolve.py --wish "add --schedule flag for cron" --target 20k --no-pr
"""

import argparse
import os
import sys
import json
import time
import random
import subprocess
import textwrap

from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("Error: pip install openai")
    sys.exit(1)


# ── Config ────────────────────────────────────────────────────────────────────

SOURCE_FILE = Path(__file__).parent / "burn.py"
CHANGES_FILE = Path(__file__).parent / "CHANGES.md"
MAX_RETRIES = 3


def parse_args():
    parser = argparse.ArgumentParser(
        description="token-sisyphus evolve — AI-driven self-improvement pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python evolve.py --wish "add email summary after run" --target 30k
  python evolve.py --wish "support concurrent requests" --target 50k
  python evolve.py --wish "add --schedule flag for cron" --target 20k --dry-run
        """,
    )
    parser.add_argument("--wish", required=True,
        help="What you want the tool to do differently")
    parser.add_argument("--target", default="30k",
        help="Target token count to consume during evolution (default: 30k)")
    parser.add_argument("--model", default="gpt-4o-mini",
        help="Model to use for all agents (default: gpt-4o-mini)")
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--base-url", default=None)
    parser.add_argument("--api", default="completions",
        choices=["completions", "responses"],
        help="OpenAI API type: completions (default) or responses (for gpt-5.x)")
    parser.add_argument("--no-pr", action="store_true",
        help="Skip opening a GitHub PR")
    parser.add_argument("--dry-run", action="store_true",
        help="Simulate pipeline without real API calls or git operations")
    return parser.parse_args()


def parse_target(s: str) -> int:
    s = s.lower().strip()
    if s.endswith("m"):
        return int(float(s[:-1]) * 1_000_000)
    elif s.endswith("k"):
        return int(float(s[:-1]) * 1_000)
    return int(s)


# ── LLM client ────────────────────────────────────────────────────────────────

def make_client(api_key, base_url):
    kwargs = {"api_key": api_key or os.environ.get("OPENAI_API_KEY", "")}
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)


def call(client, model, system, user, label="", token_counter=None, use_responses_api=False):
    """Single LLM call. Supports both chat/completions and Responses API."""
    if label:
        print(f"  → {label}...", end="", flush=True)

    if use_responses_api:
        resp = client.responses.create(
            model=model,
            input=f"{system}\n\n{user}",
            max_output_tokens=4000,
        )
        # SDK may return str on some proxy implementations — fall through to attr access
        if isinstance(resp, str):
            text = resp
            tokens = 0
        else:
            text = resp.output_text or ""
            usage = resp.usage
            tokens = ((getattr(usage, 'input_tokens', 0) +
                       getattr(usage, 'output_tokens', 0)) if usage else 0)
    else:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": user},
            ],
            max_tokens=4000,
        )
        text = resp.choices[0].message.content or ""
        tokens = resp.usage.total_tokens if resp.usage else 0

    if token_counter is not None:
        token_counter[0] += tokens
    if label:
        print(f" ✓ ({tokens} tokens)")
    return text


def pad_tokens(client, model, current, target, token_counter, use_responses_api=False):
    """Burn remaining tokens with lightweight calls if we're under target."""
    pad_prompts = [
        "List three interesting properties of Python generators.",
        "What are the tradeoffs between async and threading in Python?",
        "Explain the difference between a list and a deque briefly.",
        "What makes a good commit message?",
        "Name two underrated standard library modules in Python.",
        "What is the difference between a process and a thread?",
        "Why does Python's GIL exist and when does it matter?",
    ]
    while current < target:
        prompt = random.choice(pad_prompts)
        call(client, model, "You are a helpful assistant.", prompt,
             label=f"padding ({current:,}/{target:,})", token_counter=token_counter,
             use_responses_api=use_responses_api)
        current = token_counter[0]
        time.sleep(0.3)


# ── Patch helpers ─────────────────────────────────────────────────────────────

def apply_search_replace(original: str, patch_text: str) -> tuple[str, int]:
    """
    Apply SEARCH/REPLACE blocks to original source.
    Returns (patched_text, n_applied).
    Each block format:
        SEARCH:
        <exact lines>
        REPLACE:
        <new lines>
        END
    """
    result = original
    applied = 0

    # Parse blocks
    blocks = []
    i = 0
    lines = patch_text.splitlines()
    while i < len(lines):
        if lines[i].strip() == "SEARCH:":
            search_lines = []
            i += 1
            while i < len(lines) and lines[i].strip() != "REPLACE:":
                search_lines.append(lines[i])
                i += 1
            replace_lines = []
            i += 1  # skip REPLACE:
            while i < len(lines) and lines[i].strip() != "END":
                replace_lines.append(lines[i])
                i += 1
            blocks.append(("\n".join(search_lines), "\n".join(replace_lines)))
        i += 1

    for search, replace in blocks:
        if search in result:
            result = result.replace(search, replace, 1)
            applied += 1

    return result, applied


# ── Agents ────────────────────────────────────────────────────────────────────

def agent_pm(client, model, wish, source_code, token_counter, dry_run, use_responses_api=False):
    """PM Agent: decompose a complex wish into ordered single-point sub-tasks."""
    print("\n[0/4] 🎯  PM — decomposing wish into atomic sub-tasks")
    if dry_run:
        print("  → (dry run, skipping)")
        return [wish]

    system = textwrap.dedent("""
        You are a technical product manager reviewing a feature request for a Python CLI tool.
        Your job: decompose the wish into an ordered list of ATOMIC sub-tasks.

        Rules:
        - Each sub-task must touch at most 1-2 locations in the source code
        - Each sub-task must be independently implementable via a single SEARCH/REPLACE patch
        - Order them by dependency (earlier tasks may be required by later ones)
        - If the wish is already atomic (single location change), return it as-is as one task
        - Format: return a numbered list, one task per line, starting with "1. ", "2. ", etc.
        - Each task description must be specific enough that a developer knows exactly which lines to change
        - Maximum 5 sub-tasks

        Example output for "add --output json flag":
        1. Add `parser.add_argument('--output', choices=['json'], default=None)` in parse_args() after the last add_argument call
        2. Add `start_time = time.time()` in main() on the line before `while True:`
        3. Add JSON summary print in main() right after the `while True:` loop ends: `if args.output == 'json': print(json.dumps({...}))`
    """)
    user = (
        f"Feature wish: {wish}\n\n"
        f"Current source:\n```python\n{source_code}\n```\n\n"
        "Output the numbered sub-task list:"
    )
    result = call(client, model, system, user, "decomposing wish", token_counter, use_responses_api)

    # Parse numbered list into sub-tasks
    sub_tasks = []
    for line in result.splitlines():
        line = line.strip()
        import re
        m = re.match(r'^\d+\.\s+(.+)$', line)
        if m:
            sub_tasks.append(m.group(1).strip())

    if not sub_tasks:
        # fallback: treat whole wish as one task
        sub_tasks = [wish]

    print(f"  → {len(sub_tasks)} sub-task(s) identified")
    for i, t in enumerate(sub_tasks, 1):
        print(f"      {i}. {t[:80]}{'...' if len(t) > 80 else ''}")
    return sub_tasks


def agent_architect(client, model, wish, source_code, token_counter, dry_run, use_responses_api=False):
    print("\n[1/4] 🏗  Architect — analyzing wish and designing solution")
    if dry_run:
        print("  → (dry run, skipping)")
        return "Simulated design plan: add the requested feature cleanly."

    system = textwrap.dedent("""
        You are a senior software architect reviewing a Python CLI tool.
        Your job: given a feature wish, produce a concise design plan (max 250 words).
        Be extremely specific:
        - Quote the exact function name(s) that need to change
        - Quote the exact argparse argument(s) to add (name, type, default)
        - Quote the exact location in main() where new logic goes
        - List edge cases to handle
        No code yet, just the plan.
    """)
    user = f"Current tool source:\n\n```python\n{source_code}\n```\n\nFeature wish: {wish}"
    return call(client, model, system, user, "designing solution", token_counter, use_responses_api)


def agent_coder(client, model, wish, source_code, design_plan, token_counter, dry_run, use_responses_api=False):
    print("\n[2/4] 💻  Coder — generating patch")
    if dry_run:
        print("  → (dry run, skipping)")
        return "SEARCH:\n#!/usr/bin/env python3\nREPLACE:\n#!/usr/bin/env python3\n# evolve: simulated change\n"

    system = textwrap.dedent("""
        You are an expert Python developer. Given original source code and a design plan,
        produce one or more SEARCH/REPLACE blocks to implement the requested feature.

        Format — repeat for each change:
        SEARCH:
        <exact lines from the original file to find, verbatim>
        REPLACE:
        <new lines to substitute in>
        END

        Rules:
        - SEARCH must be an exact verbatim copy of lines from the original (whitespace matters)
        - SEARCH block should be 2-5 lines that uniquely identify the location
        - REPLACE contains the full replacement (can be more or fewer lines than SEARCH)
        - Output ONLY the SEARCH/REPLACE blocks, no explanation, no markdown fences
        - If adding new code at the end of a function, use the last 2 lines of that function as SEARCH
        - NEVER write recursive calls (a function calling itself)
        - Loop logic must use while/for, not recursion
        - New scheduling logic must go inside main(), not in a separate helper that calls main()
        - If the feature requires changes in MULTIPLE places (argparse + function body + main), output ALL of them as separate SEARCH/REPLACE blocks — do NOT omit any part
    """)
    user = (
        f"Design plan:\n{design_plan}\n\n"
        f"Feature wish: {wish}\n\n"
        f"Original source (burn.py):\n```python\n{source_code}\n```\n\n"
        "Output the SEARCH/REPLACE blocks:"
    )
    return call(client, model, system, user, "generating patch", token_counter, use_responses_api)


def agent_reviewer(client, model, wish, source_code, patch_text, token_counter, dry_run, use_responses_api=False):
    print("\n[3/4] 🔍  Reviewer — reviewing patch")
    if dry_run:
        print("  → (dry run, skipping)")
        return "PASS: simulated review passed."

    system = textwrap.dedent("""
        You are a critical code reviewer. Review these SEARCH/REPLACE blocks for a Python CLI tool.
        Check:
        1. Correctness — do the changes implement the wish properly?
        2. Safety — no shell injection, no hardcoded secrets, no destructive ops
        3. Backwards compatibility — existing CLI flags still work
        4. Completeness — are all necessary changes included?

        The source imports section shows what modules are already imported — do NOT fail for missing imports if they already exist there.

        Respond with either:
        PASS: <brief reason>
        FAIL: <specific problems to fix>
    """)
    # Give reviewer context: imports from source + full patch
    import_section = "\n".join(source_code.splitlines()[:35])  # imports + early constants
    user = (
        f"Feature wish: {wish}\n\n"
        f"Source imports (for reference):\n```python\n{import_section}\n```\n\n"
        f"SEARCH/REPLACE blocks:\n{patch_text}"
    )
    return call(client, model, system, user, "reviewing patch", token_counter, use_responses_api)


def agent_tester(client, model, wish, patch_text, token_counter, dry_run, use_responses_api=False):
    print("\n[4/4] 🧪  Tester — generating test cases")
    if dry_run:
        print("  → (dry run, skipping)")
        return "Simulated test cases: all pass."

    system = textwrap.dedent("""
        You are a QA engineer. Given SEARCH/REPLACE code changes for a Python CLI tool and a feature wish,
        write 3-5 concrete CLI test cases (as bash commands with expected behavior).
        Focus on the new feature and regression of existing flags.
        Format: one test per line, starting with `# test:` comment then the command.
    """)
    user = f"Feature wish: {wish}\n\nCode changes:\n{patch_text}"
    return call(client, model, system, user, "generating tests", token_counter, use_responses_api)


# ── Output ────────────────────────────────────────────────────────────────────

def write_outputs(patch_text, design_plan, review_result, test_cases, wish):
    changes = textwrap.dedent(f"""
        # CHANGES — {datetime.now().strftime('%Y-%m-%d')}

        ## Wish
        {wish}

        ## Design Plan
        {design_plan}

        ## Patch Applied
        ```
        {patch_text}
        ```

        ## Review Result
        {review_result}

        ## Generated Test Cases
        {test_cases}
    """).strip()
    CHANGES_FILE.write_text(changes)
    print(f"  ✅ Written: {CHANGES_FILE.name}")


def open_pr(wish, dry_run):
    branch = f"evolve/{wish[:40].lower().replace(' ', '-').replace('/', '-')}"
    branch = "".join(c for c in branch if c.isalnum() or c in "-/")

    if dry_run:
        print(f"\n  (dry run) Would open PR on branch: {branch}")
        return

    print(f"\n  Opening PR on branch: {branch}")
    cmds = [
        ["git", "checkout", "-b", branch],
        ["git", "add", str(SOURCE_FILE), str(CHANGES_FILE)],
        ["git", "commit", "-m", f"evolve: {wish[:60]}"],
        ["git", "push", "-u", "origin", branch],
        ["gh", "pr", "create",
         "--title", f"evolve: {wish[:60]}",
         "--body", CHANGES_FILE.read_text(),
         "--base", "main"],
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, capture_output=True, text=True,
                                cwd=str(SOURCE_FILE.parent))
        if result.returncode != 0:
            print(f"  ⚠️  {' '.join(cmd[:2])} failed: {result.stderr.strip()}")
            return
    print("  ✅ PR opened successfully")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args = parse_args()
    target = parse_target(args.target)
    original_source = SOURCE_FILE.read_text()
    token_counter = [0]

    print(f"\n🪨  token-sisyphus evolve mode")
    print(f"    Wish   : {args.wish}")
    print(f"    Target : {target:,} tokens")
    print(f"    Model  : {args.model}")
    print(f"    Mode   : {'DRY RUN' if args.dry_run else 'LIVE'}\n")

    client = None if args.dry_run else make_client(args.api_key, args.base_url)
    use_responses = (args.api == "responses")

    # PM: decompose wish into atomic sub-tasks
    sub_tasks = agent_pm(client, args.model, args.wish, original_source, token_counter, args.dry_run, use_responses)

    source_code = original_source
    all_diffs = []
    all_designs = []
    all_reviews = []
    all_tests = []

    for task_idx, sub_wish in enumerate(sub_tasks, 1):
        if len(sub_tasks) > 1:
            print(f"\n{'─'*60}")
            print(f"  Sub-task {task_idx}/{len(sub_tasks)}: {sub_wish[:70]}{'...' if len(sub_wish)>70 else ''}")

        final_diff = None
        final_patched = None

        for attempt in range(1, MAX_RETRIES + 1):
            design   = agent_architect(client, args.model, sub_wish, source_code, token_counter, args.dry_run, use_responses)
            diff_raw = agent_coder(client, args.model, sub_wish, source_code, design, token_counter, args.dry_run, use_responses)
            review   = agent_reviewer(client, args.model, sub_wish, source_code, diff_raw, token_counter, args.dry_run, use_responses)
            tests    = agent_tester(client, args.model, sub_wish, diff_raw, token_counter, args.dry_run, use_responses)

            passed = args.dry_run or review.strip().upper().startswith("PASS")

            if not args.dry_run:
                patched, n_applied = apply_search_replace(source_code, diff_raw)
                if n_applied == 0:
                    print(f"\n  ⚠️  No SEARCH blocks matched source (attempt {attempt}/{MAX_RETRIES})")
                    if attempt == MAX_RETRIES:
                        print(f"\n  Sub-task {task_idx} failed. Writing failure report.")
                        Path("FAILED.md").write_text(
                            f"# Evolve failed\n\nSub-task {task_idx}: {sub_wish}\n\nNo SEARCH blocks matched.\n\nPatch:\n{diff_raw}\n\nReview:\n{review}"
                        )
                        sys.exit(1)
                    continue
                diff_text = diff_raw
            else:
                diff_text = diff_raw
                patched = source_code + f"\n# evolve: sub-task {task_idx} simulated\n"

            if passed:
                print(f"\n  Review: ✅ PASS")
                final_diff = diff_text
                final_patched = patched
                break
            else:
                print(f"\n  Review: ❌ FAIL (attempt {attempt}/{MAX_RETRIES})")
                print(f"  Reason: {review[:200]}")
                if attempt == MAX_RETRIES:
                    print(f"\n  Sub-task {task_idx} failed after {MAX_RETRIES} attempts.")
                    Path("FAILED.md").write_text(
                        f"# Evolve failed\n\nSub-task {task_idx}: {sub_wish}\n\nReview:\n{review}"
                    )
                    sys.exit(1)
                source_code = patched  # feed patched back for retry

        # Accumulate
        all_diffs.append(final_diff)
        all_designs.append(design)
        all_reviews.append(review)
        all_tests.append(tests)

        # Apply sub-task patch to live source for next sub-task
        if not args.dry_run and final_patched:
            source_code = final_patched
            SOURCE_FILE.write_text(final_patched)
            print(f"  ✅ Patched: {SOURCE_FILE.name} (sub-task {task_idx}/{len(sub_tasks)})")

    final_diff = "\n\n---\n\n".join(d for d in all_diffs if d)

    # Pad to target token count if needed
    if not args.dry_run and token_counter[0] < target:
        print(f"\n  Padding to target ({token_counter[0]:,} / {target:,} tokens)...")
        pad_tokens(client, args.model, token_counter[0], target, token_counter, use_responses)

    # Write CHANGES.md
    print(f"\n  Writing outputs...")
    write_outputs(final_diff, "\n\n---\n\n".join(all_designs),
                  "\n\n---\n\n".join(all_reviews), "\n\n---\n\n".join(all_tests), args.wish)

    # Open PR
    if not args.no_pr:
        open_pr(args.wish, args.dry_run)

    print(f"\n✅  Done. Total tokens: {token_counter[0]:,}")
    print(f"    Your boulder has reached the top. And it wrote its own successor.\n")


if __name__ == "__main__":
    main()
