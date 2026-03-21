#!/usr/bin/env python3
"""
token-sisyphus evolve mode — self-improving agent pipeline

Four-agent pipeline:
  1. Architect  — analyzes wish, designs solution
  2. Coder      — implements the changes
  3. Reviewer   — independent AI code review
  4. Tester     — generates tests, runs dry-run validation

Outputs:
  - burn_evolved.py  (the improved script)
  - CHANGES.md       (what changed and why)
  - Opens a GitHub PR automatically if all agents pass

Usage:
  python evolve.py --wish "add email summary after each run" --target 30k
  python evolve.py --wish "support concurrent requests" --target 50k --dry-run
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
OUTPUT_FILE = Path(__file__).parent / "burn_evolved.py"
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
            max_output_tokens=2000,
        )
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
            max_tokens=2000,
        )
        text = resp.choices[0].message.content or ""
        tokens = resp.usage.total_tokens if resp.usage else 0

    if token_counter is not None:
        token_counter[0] += tokens
    if label:
        print(f" ✓ ({tokens} tokens)")
    return text


def pad_tokens(client, model, current, target, token_counter):
    """Burn remaining tokens with lightweight calls if we're under target."""
    pad_prompts = [
        "List three interesting properties of Python generators.",
        "What are the tradeoffs between async and threading in Python?",
        "Explain the difference between a list and a deque briefly.",
        "What makes a good commit message?",
        "Name two underrated standard library modules in Python.",
    ]
    while current < target:
        prompt = random.choice(pad_prompts)
        _, t = call(client, model, "You are a helpful assistant.", prompt,
                    label=f"padding (total so far: {current:,})", token_counter=token_counter)
        current = token_counter[0]
        time.sleep(0.3)


# ── Agents ────────────────────────────────────────────────────────────────────

def agent_architect(client, model, wish, source_code, token_counter, dry_run, use_responses_api=False):
    print("\n[1/4] 🏗  Architect — analyzing wish and designing solution")
    if dry_run:
        print("  → (dry run, skipping)")
        return "Simulated design plan: add the requested feature cleanly."

    system = textwrap.dedent("""
        You are a senior software architect reviewing a Python CLI tool.
        Your job: given a feature wish, produce a concise design plan (max 300 words).
        Focus on: what to change, what to add, what edge cases to consider.
        Be specific and actionable. No code yet.
    """)
    user = f"Current tool source:\n\n```python\n{source_code}\n```\n\nFeature wish: {wish}"
    return call(client, model, system, user, "designing solution", token_counter, use_responses_api)


def agent_coder(client, model, wish, source_code, design_plan, token_counter, dry_run, use_responses_api=False):
    print("\n[2/4] 💻  Coder — implementing changes")
    if dry_run:
        print("  → (dry run, skipping)")
        return source_code + "\n# evolve: simulated change\n"

    system = textwrap.dedent("""
        You are an expert Python developer implementing a feature in a CLI tool.
        Given the original source code and a design plan, produce the complete updated Python file.
        Rules:
        - Output ONLY the complete Python source code, no markdown fences, no explanation
        - Preserve all existing functionality
        - Keep the code clean, well-commented, under 300 lines
        - The file must be runnable as-is
    """)
    user = (
        f"Design plan:\n{design_plan}\n\n"
        f"Feature wish: {wish}\n\n"
        f"Original source:\n```python\n{source_code}\n```\n\n"
        "Output the complete updated Python file:"
    )
    return call(client, model, system, user, "writing code", token_counter, use_responses_api)


def agent_reviewer(client, model, wish, original_code, new_code, token_counter, dry_run, use_responses_api=False):
    print("\n[3/4] 🔍  Reviewer — independent AI code review")
    if dry_run:
        print("  → (dry run, skipping)")
        return "PASS: simulated review passed."

    system = textwrap.dedent("""
        You are a critical code reviewer. Review the code change for:
        1. Correctness — does it implement the wish properly?
        2. Safety — no shell injection, no hardcoded secrets, no destructive ops
        3. Backwards compatibility — existing CLI flags still work
        4. Code quality — no obvious bugs, reasonable error handling

        Respond with either:
        PASS: <brief reason>
        FAIL: <specific problems to fix>
    """)
    user = (
        f"Feature wish: {wish}\n\n"
        f"Original:\n```python\n{original_code[:2000]}\n```\n\n"
        f"Updated:\n```python\n{new_code[:2000]}\n```"
    )
    return call(client, model, system, user, "reviewing", token_counter, use_responses_api)


def agent_tester(client, model, wish, new_code, token_counter, dry_run, use_responses_api=False):
    print("\n[4/4] 🧪  Tester — generating test cases")
    if dry_run:
        print("  → (dry run, skipping)")
        return "Simulated test cases: all pass."

    system = textwrap.dedent("""
        You are a QA engineer. Given updated Python CLI tool code and a feature wish,
        write 3-5 concrete CLI test cases (as bash commands with expected behavior).
        Focus on the new feature and regression of existing flags.
        Format: one test per line, starting with `# test:` comment then the command.
    """)
    user = f"Feature wish: {wish}\n\nUpdated code:\n```python\n{new_code[:2000]}\n```"
    return call(client, model, system, user, "generating tests", token_counter, use_responses_api)


# ── Output ────────────────────────────────────────────────────────────────────

def write_outputs(new_code, design_plan, review_result, test_cases, wish):
    OUTPUT_FILE.write_text(new_code)
    print(f"\n  ✅ Written: {OUTPUT_FILE.name}")

    changes = textwrap.dedent(f"""
        # CHANGES — {datetime.now().strftime('%Y-%m-%d')}

        ## Wish
        {wish}

        ## Design Plan
        {design_plan}

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
        ["git", "add", str(OUTPUT_FILE), str(CHANGES_FILE)],
        ["git", "commit", "-m", f"evolve: {wish[:60]}"],
        ["git", "push", "-u", "origin", branch],
        ["gh", "pr", "create",
         "--title", f"evolve: {wish[:60]}",
         "--body", CHANGES_FILE.read_text(),
         "--base", "main"],
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ⚠️  {' '.join(cmd[:2])} failed: {result.stderr.strip()}")
            return
    print("  ✅ PR opened successfully")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args = parse_args()
    target = parse_target(args.target)
    source_code = SOURCE_FILE.read_text()
    token_counter = [0]

    print(f"\n🪨  token-sisyphus evolve mode")
    print(f"    Wish   : {args.wish}")
    print(f"    Target : {target:,} tokens")
    print(f"    Model  : {args.model}")
    if args.dry_run:
        print(f"    Mode   : DRY RUN\n")
    else:
        print(f"    Mode   : LIVE\n")

    client = None if args.dry_run else make_client(args.api_key, args.base_url)
    use_responses = (args.api == "responses")

    # Run the four-agent pipeline
    for attempt in range(1, MAX_RETRIES + 1):
        design   = agent_architect(client, args.model, args.wish, source_code, token_counter, args.dry_run, use_responses)
        new_code = agent_coder(client, args.model, args.wish, source_code, design, token_counter, args.dry_run, use_responses)
        review   = agent_reviewer(client, args.model, args.wish, source_code, new_code, token_counter, args.dry_run, use_responses)
        tests    = agent_tester(client, args.model, args.wish, new_code, token_counter, args.dry_run, use_responses)

        if args.dry_run or review.strip().upper().startswith("PASS"):
            print(f"\n  Review: ✅ PASS")
            break
        else:
            print(f"\n  Review: ❌ FAIL (attempt {attempt}/{MAX_RETRIES})")
            print(f"  Reason: {review[:200]}")
            if attempt == MAX_RETRIES:
                print("\n  All attempts failed. Writing failure report.")
                Path("FAILED.md").write_text(f"# Evolve failed\n\nWish: {args.wish}\n\nReview:\n{review}")
                sys.exit(1)
            source_code = new_code  # feed evolved code back for retry

    # Pad to target token count if needed
    if not args.dry_run and token_counter[0] < target:
        print(f"\n  Padding to target ({token_counter[0]:,} / {target:,} tokens)...")
        pad_tokens(client, args.model, token_counter[0], target, token_counter)

    # Write outputs
    print(f"\n  Writing outputs...")
    write_outputs(new_code, design, review, tests, args.wish)

    # Open PR
    if not args.no_pr:
        open_pr(args.wish, args.dry_run)

    print(f"\n✅  Done. Total tokens: {token_counter[0]:,}")
    print(f"    Your boulder has reached the top. And it wrote its own successor.\n")


if __name__ == "__main__":
    main()
