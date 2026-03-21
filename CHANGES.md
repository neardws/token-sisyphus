# CHANGES — 2026-03-21

        ## Wish
        add a --schedule flag so the tool runs automatically every N minutes using time.sleep

        ## Design Plan
        Plan:

- Change `"parse_args()"` to add:
  - `"--schedule"`, `type=float`, `default=0`
  - Help text: run continuously, starting a new burn cycle every N minutes; `0` means disabled.

- Change `"main()"` only; no provider function signatures need to change because scheduling wraps the existing single-run behavior.

- In `"main()"`, insert validation logic immediately after:
  - `"args = parse_args()"`
  - before `"target = parse_target(args.target)"`
  - Validate `args.schedule >= 0`; reject negative values with `argparse` error or explicit `SystemExit`.
  - Optionally reject absurdly small positive values (e.g. `< 0.1`) if you want to prevent tight loops.

- In `"main()"`, keep the existing startup summary, but add one line after:
  - `print(f"    Model    : {model}")`
  - showing schedule mode when `args.schedule > 0`, e.g. “Schedule : every N minutes”.

- In `"main()"`, replace the current provider-dispatch block starting at:
  - `if args.provider == "openai":`
  - and ending at the final `"burn_gemini(...)"`,
  - with a single-cycle helper flow inside a loop:
    - Run one burn cycle using the existing provider dispatch.
    - If `args.schedule == 0`, break.
    - Otherwise `time.sleep(args.schedule * 60)` and repeat.

- Best structure: add a small nested helper inside `"main()"` (or a new top-level function like `"run_once(args, target, model)"`) containing the current provider dispatch.

Edge cases to handle:
- `--schedule 0` preserves current one-shot behavior.
- Negative schedule values.
- Fractional minutes (`0.5` = 30 seconds).
- KeyboardInterrupt during burn cycle or during the sleep between cycles.
- Drift: sleep occurs after cycle completion, so interval is “N minutes after previous run ends,” not wall-clock aligned.
- Repeated live runs should not re-parse args or mutate target/model.

        ## Patch Applied
        ```
        SEARCH:
    parser.add_argument("--delay", type=float, default=0.5,
        help="Delay between requests in seconds (default: 0.5)")
    parser.add_argument("--dry-run", action="store_true",
        help="Simulate without real API calls")
REPLACE:
    parser.add_argument("--delay", type=float, default=0.5,
        help="Delay between requests in seconds (default: 0.5)")
    parser.add_argument("--schedule", type=float, default=0,
        help="Run continuously, starting a new burn cycle every N minutes; 0 means disabled")
    parser.add_argument("--dry-run", action="store_true",
        help="Simulate without real API calls")
END
SEARCH:
def main():
    args = parse_args()
    target = parse_target(args.target)
    model = args.model or PROVIDER_DEFAULTS[args.provider]
REPLACE:
def main():
    args = parse_args()
    if args.schedule < 0:
        raise SystemExit("Error: --schedule must be >= 0")
    if 0 < args.schedule < 0.1:
        raise SystemExit("Error: --schedule must be 0 or at least 0.1 minutes")
    target = parse_target(args.target)
    model = args.model or PROVIDER_DEFAULTS[args.provider]
END
SEARCH:
    print(f"    Target   : {target:,} tokens")
    print(f"    Model    : {model}")
    if args.dry_run:
        print(f"    Mode     : DRY RUN (no real API calls)\n")
REPLACE:
    print(f"    Target   : {target:,} tokens")
    print(f"    Model    : {model}")
    if args.schedule > 0:
        print(f"    Schedule : every {args.schedule:g} minutes")
    if args.dry_run:
        print(f"    Mode     : DRY RUN (no real API calls)\n")
END
SEARCH:
    if args.provider == "openai":
        burn_openai(target, model, args.api_key, args.base_url,
                    args.max_tokens, args.delay, args.dry_run,
                    use_responses_api=(args.api == "responses"))
    elif args.provider == "claude":
        burn_claude(target, model, args.api_key,
                    args.max_tokens, args.delay, args.dry_run)
    elif args.provider == "gemini":
        burn_gemini(target, model, args.api_key,
                    args.max_tokens, args.delay, args.dry_run)
REPLACE:
    def run_once():
        if args.provider == "openai":
            burn_openai(target, model, args.api_key, args.base_url,
                        args.max_tokens, args.delay, args.dry_run,
                        use_responses_api=(args.api == "responses"))
        elif args.provider == "claude":
            burn_claude(target, model, args.api_key,
                        args.max_tokens, args.delay, args.dry_run)
        elif args.provider == "gemini":
            burn_gemini(target, model, args.api_key,
                        args.max_tokens, args.delay, args.dry_run)

    while True:
        try:
            run_once()
            if args.schedule == 0:
                break
            print(f"⏲️  Next burn cycle starts in {args.schedule:g} minutes. Press Ctrl+C to stop.")
            time.sleep(args.schedule * 60)
        except KeyboardInterrupt:
            print("\n\nStopped by user.")
            break
END
        ```

        ## Review Result
        PASS: Adds a `--schedule` flag with validation, preserves existing flags/behavior when omitted (`0` means disabled), and implements repeated runs via `time.sleep` without introducing obvious safety issues.

        ## Generated Test Cases
        # test: python tool.py 1000 --provider openai --dry-run; expected: exits 0 after a single burn cycle, does not print any "Schedule :" or "Next burn cycle starts" message, preserving existing non-scheduled behavior
# test: python tool.py 1000 --provider openai --dry-run --schedule 1; expected: prints "Schedule : every 1 minutes", runs one dry-run cycle, then prints "Next burn cycle starts in 1 minutes. Press Ctrl+C to stop." and remains running/sleeping until interrupted
# test: python tool.py 1000 --provider openai --dry-run --schedule -1; expected: exits non-zero immediately with "Error: --schedule must be >= 0" before starting any burn cycle
# test: python tool.py 1000 --provider openai --dry-run --schedule 0.05; expected: exits non-zero immediately with "Error: --schedule must be 0 or at least 0.1 minutes" before starting any burn cycle
# test: timeout 2s python tool.py 1000 --provider openai --dry-run --delay 0.2 --schedule 0.1; expected: starts successfully, includes both dry-run mode output and "Schedule : every 0.1 minutes", showing --delay/--dry-run still work alongside --schedule; process is terminated by timeout before the next cycle begins