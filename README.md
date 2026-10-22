# Ticket: Automated PR review agent (prototype)

Our team reviews every pull request against a short checklist (`checklist.md`). Reviewers spend a lot of time on the mechanical part of that, and they still miss things.

Build an AI agent that reviews a folder of PR diffs against the checklist, unattended, and reports what it finds.

For each diff, the agent should:

1. Find violations of the checklist rules, with the rule, file, and line.
2. Write a short review comment for each finding that a developer could act on.
3. Give the PR a verdict:
   * `approve` if it found no violations
   * `request_changes` if it found any
   * `needs_human` if it could not review the PR reliably

The agent must use an LLM for the review. Deterministic checks alongside it are fine.

Treat this as a prototype the team might eventually run on every real PR.

## What's here

| Path | What it is |
|---|---|
| `checklist.md` | The review rules. Only these rules count. Don't change this file. |
| `samples/` | Two example diffs (`git format-patch` output) |
| `samples/expected.json` | What a correct review of the samples looks like, in the output format |
| `tools/ado_review.py` | Our Azure DevOps review client, if you want it |
| `output/` | Where results go |

## Input and output

**Input:** a folder of `.diff` files. Your agent must take the folder path as an argument. At the end of the session you'll run it on a different folder of diffs that you haven't seen.

**Output:** one JSON file, by default `output/results.json`:

```json
{
  "reviews": [
    {
      "diff": "pr-0901.diff",
      "verdict": "request_changes",
      "findings": [
        {
          "rule": "R2",
          "file": "src/Contoso.Claims/Data/ClaimRepository.cs",
          "line": 27,
          "comment": "lastName is interpolated into the SQL text. Pass it as a parameter."
        }
      ]
    }
  ]
}
```

* `diff` is the file name of the diff.
* `rule` is a checklist rule ID (`R1` to `R7`).
* `file` is the path as it appears in the diff.
* `line` is the line number in the **new** version of the file (the `+` side of the diff).
* Include every diff in `reviews`, even ones with no findings.

Put the one command that runs your agent at the top of a `RUN.md` file.

## Ground rules

* Clone this repo or download it as a zip. **Please don't fork it or use it as a template.** Forks are public, so other candidates could see your work.
* Use any language, framework, AI tools, and LLM provider. You're expected to use AI tools to build this.
* Searching the web and reading documentation is fine.
* Ask us questions at any time. Thinking out loud helps us follow your reasoning.
* We'll hand you something new a couple of times during the build, the way requirements change on a real ticket.
* You have about 40 minutes. A working agent that you understand beats an ambitious one that doesn't run.
* At the end, you'll send us your `results.json` and a zip of this whole folder.
