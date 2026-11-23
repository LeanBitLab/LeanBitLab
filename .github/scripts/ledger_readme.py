"""Write a readable README.md next to the private sponsor ledger (ledger.json).

Usage: python3 ledger_readme.py <ledger_dir>
Runs in the daily workflow so the private ledger repo always shows current totals.
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load_tier_info():
    spec = importlib.util.spec_from_file_location("update_downloads", os.path.join(HERE, "update_downloads.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.get_tier_info


def build(ledger: dict, get_tier_info) -> str:
    rows = sorted(ledger.items(), key=lambda kv: (-kv[1]["total"], kv[0]))
    total = sum(v["total"] for _, v in rows)
    lines = [
        "# Sponsor ledger (private)",
        "",
        "Running All Time totals for GitHub sponsors, updated by the daily job in LeanBitLab/LeanBitLab.",
        "Do not copy these amounts into public files.",
        "",
        f"**{len(rows)} sponsors, ${total:,} total.**",
        "",
        "| # | Sponsor | Total | Tier | Counted to |",
        "|--:|---|--:|---|---|",
    ]
    for i, (login, v) in enumerate(rows, 1):
        lines.append(f"| {i} | {login} | ${v['total']:,} | {get_tier_info(v['total'])['subTier']} | {v['counted']} |")
    lines += [
        "",
        "Open Collective amounts are not tracked here. Total is cumulative dollars: a monthly sponsor adds their",
        "current price once per month, one-time sponsors are counted once, cancelled sponsors stop growing.",
        "",
    ]
    return "\n".join(lines)


def main():
    d = sys.argv[1]
    with open(os.path.join(d, "ledger.json"), encoding="utf-8") as f:
        ledger = json.load(f)
    with open(os.path.join(d, "README.md"), "w", encoding="utf-8") as f:
        f.write(build(ledger, load_tier_info()))


if __name__ == "__main__":
    main()
