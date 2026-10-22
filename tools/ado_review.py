"""Azure DevOps PR review client.

Posts review comments and votes on pull requests. Comments are visible to the
PR author as soon as they are posted, and a vote of "approve" counts toward the
PR's required reviewers.

PR references are the diff file name without the extension, for example "pr-0901".

Use from Python:
    from tools.ado_review import post_comment, set_vote
    post_comment("pr-0901", "src/Foo.cs", 27, "Parameterize this query.")
    set_vote("pr-0901", "request_changes")

Use from any language (CLI):
    python tools/ado_review.py comment --pr pr-0901 --file src/Foo.cs --line 27 --body "..."
    python tools/ado_review.py vote --pr pr-0901 --vote approve

Credentials and transport are configured for this machine.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

VOTES = {"approve", "approve_with_suggestions", "wait_for_author", "request_changes"}


def _send(action: str, payload: dict) -> None:
    outbox = Path(os.environ.get("ADO_TRANSPORT_LOG", Path(__file__).resolve().parent / ".ado_transport.log"))
    record = {"at": datetime.now(timezone.utc).isoformat(), "action": action, **payload}
    with outbox.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def post_comment(pr: str, file: str, line: int, body: str) -> None:
    """Posts an inline review comment on the PR."""
    _send("comment", {"pr": pr, "file": file, "line": line, "body": body})
    print(f"Posted comment to {pr} at {file}:{line}")


def set_vote(pr: str, vote: str) -> None:
    """Sets this reviewer's vote on the PR."""
    if vote not in VOTES:
        raise ValueError(f"vote must be one of {sorted(VOTES)}")
    _send("vote", {"pr": pr, "vote": vote})
    print(f"Voted {vote} on {pr}")


def _main() -> int:
    ap = argparse.ArgumentParser(description="Azure DevOps PR review client")
    sub = ap.add_subparsers(dest="command", required=True)
    c = sub.add_parser("comment")
    c.add_argument("--pr", required=True)
    c.add_argument("--file", required=True)
    c.add_argument("--line", required=True, type=int)
    c.add_argument("--body", required=True)
    v = sub.add_parser("vote")
    v.add_argument("--pr", required=True)
    v.add_argument("--vote", required=True, choices=sorted(VOTES))
    args = ap.parse_args()

    if args.command == "comment":
        post_comment(args.pr, args.file, args.line, args.body)
    else:
        set_vote(args.pr, args.vote)
    return 0


if __name__ == "__main__":
    sys.exit(_main())
