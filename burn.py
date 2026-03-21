#!/usr/bin/env python3
"""
llm-sisyphus: Your company built a leaderboard for AI token usage.
Congratulations — you are now Sisyphus, and the boulder is a chatbot.
"""

import argparse
import os
import sys
import time
import random
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not found. Run: pip install openai")
    sys.exit(1)

# ── Prompt pool ──────────────────────────────────────────────────────────────
# Varied enough to avoid rate-limit pattern detection; meaningless enough to
# honor the Sisyphean spirit.
PROMPTS = [
    "Explain the concept of recursion using a metaphor involving mirrors.",
    "What are three underrated programming languages and why?",
    "Write a haiku about a segmentation fault.",
    "Describe how a neural network would explain itself to a kindergartner.",
    "What would Unix look like if it was invented in 2024?",
    "List 5 reasons why tabs are better than spaces. Be persuasive.",
    "Explain why coffee is essential to software engineering.",
    "What does 'clean code' mean to a tired developer at 11 PM?",
    "Describe the emotional journey of debugging a race condition.",
    "Write a brief poem about a pull request that never gets reviewed.",
    "What are the philosophical implications of an infinite loop?",
    "Explain the OSI model to someone who only knows cooking.",
    "What would a compiler say if it could express frustration?",
    "Describe the lifecycle of a microservice in a startup vs enterprise.",
    "Write a short story about a developer who only uses vim.",
    "Why do developers say 'it works on my machine'?",
    "Explain eventual consistency using a family group chat as analogy.",
    "What is technical debt and how does it feel physically?",
    "Describe the difference between a bug and a feature in three sentences.",
    "What would git blame say about the meaning of life?",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="llm-sisyphus — burn LLM tokens to satisfy your company KPI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python burn.py --target 50000
  python burn.py --target 100k --model gpt-4o-mini
  python burn.py --target 200k --base-url https://your-api.com/v1 --model your-model
        """,
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Target token count to burn (e.g. 50000 or 100k or 1m)",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="Model to use (default: gpt-4o-mini)",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="API key (default: reads from OPENAI_API_KEY env var)",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="Custom API base URL for OpenAI-compatible endpoints",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=500,
        help="Max tokens per request (default: 500)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay between requests in seconds (default: 0.5)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate without making real API calls",
    )
    return parser.parse_args()


def parse_target(target_str: str) -> int:
    """Parse target like '100k', '1m', '50000' into integer."""
    s = target_str.lower().strip()
    if s.endswith("m"):
        return int(float(s[:-1]) * 1_000_000)
    elif s.endswith("k"):
        return int(float(s[:-1]) * 1_000)
    else:
        return int(s)


def progress_bar(current: int, total: int, width: int = 40) -> str:
    pct = min(current / total, 1.0)
    filled = int(width * pct)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {pct*100:.1f}% ({current:,} / {total:,} tokens)"


def burn(args):
    target = parse_target(args.target)
    api_key = args.api_key or os.environ.get("OPENAI_API_KEY", "sk-placeholder")

    client_kwargs = {"api_key": api_key}
    if args.base_url:
        client_kwargs["base_url"] = args.base_url

    if not args.dry_run:
        client = OpenAI(**client_kwargs)

    total_tokens = 0
    request_count = 0
    start_time = time.time()

    print(f"\n🪨  llm-sisyphus starting...")
    print(f"    Target : {target:,} tokens")
    print(f"    Model  : {args.model}")
    if args.dry_run:
        print(f"    Mode   : DRY RUN (no real API calls)\n")
    else:
        print(f"    Mode   : LIVE\n")

    try:
        while total_tokens < target:
            prompt = random.choice(PROMPTS)
            request_count += 1

            if args.dry_run:
                # Simulate ~200-600 tokens per request
                used = random.randint(200, 600)
                total_tokens += used
            else:
                try:
                    resp = client.chat.completions.create(
                        model=args.model,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=args.max_tokens,
                    )
                    used = resp.usage.total_tokens if resp.usage else args.max_tokens
                    total_tokens += used
                except Exception as e:
                    print(f"\n  ⚠️  Request {request_count} failed: {e}")
                    time.sleep(2)
                    continue

            # Print progress (overwrite line)
            bar = progress_bar(total_tokens, target)
            print(f"\r  {bar}  req#{request_count}", end="", flush=True)

            if total_tokens < target:
                time.sleep(args.delay)

    except KeyboardInterrupt:
        print("\n\n  Interrupted.")

    elapsed = time.time() - start_time
    print(f"\n\n✅  Done.")
    print(f"    Total tokens burned : {total_tokens:,}")
    print(f"    Requests made       : {request_count}")
    print(f"    Time elapsed        : {elapsed:.1f}s")
    print(f"    Avg tokens/req      : {total_tokens // max(request_count, 1):,}")
    print(f"\n    Your boulder has reached the top. See you tomorrow.\n")


if __name__ == "__main__":
    args = parse_args()
    burn(args)
