---
name: blackboard-submission
description: Safely prepare, review, and submit the CSCI 6032 homework archive to Blackboard only after a dry run, explicit human approval, and verification of the final confirmation page.
---

# Blackboard submission skill

Use this skill only for this homework repository and only for the Blackboard submission flow described in the assignment. The goal is to protect the student from accidental submission of the wrong archive, unpublished work, or private data while still allowing a controlled submission. Before submitting check if all homework questions are answered and are correct.

## Required repository and safety checks

1. Confirm the working directory is the expected homework repository.
   - Verify the repo root contains the required project files: `CSCI6032_hw2.ipynb`, `README.md`, `AGENTS.md`, `sample.txt`, `Dockerfile`, `src/text_stats.py`, `tests/test_text_stats.py`, and `.github/skills/blackboard-submission/SKILL.md`.
   - Confirm the remote URL matches the expected public GitHub repository for this student and assignment.
   - Confirm the current branch is the reviewed branch, not a detached HEAD or unrelated worktree.

2. Run a preflight before any browser action.
   - Check `git status --short` and stop if the tree is not clean.
   - Check recent commits (`git log --oneline -n 10`) to confirm the required checkpoints and the final reviewed state are present.
   - Confirm the branch has been pushed to the remote and is up to date with the remote tracking branch.
   - Inspect the repo for obvious secrets or personal data: `.env`, credentials, browser profile folders, tokens, SSH keys, Docker socket paths, or local MCP config containing private paths or extension tokens.
   - If any of the above fail, stop and report the problem clearly. Do not continue.

3. Require a clean, reviewed submission state.
   - The archive must be created from the committed `HEAD` only.
   - Do not include `.git`, caches, credentials, browser state, or unrelated files.
   - Do not include secrets, private information, or personal paths in the notebook or archive contents.

## Dry-run workflow

4. Support dry-run mode first, and treat dry run as the default.
   - Assume dry run unless the student explicitly asks for a real submission in this invocation.
   - Run all possible safety checks and output the exact work that would be packaged.
   - Show the proposed archive name, archive contents, repository URL, notebook path, and exact Blackboard submission text.
   - Do not open Blackboard, do not click anything, and do not submit in dry-run mode.
   - Exit with explicit findings if any check fails.

5. Prepare the submission artifact.
   - Use the committed `HEAD` state only.
   - Build the archive with `git archive`, which reads from the commit and therefore cannot include `.git`, uncommitted edits, or ignored files:

     ```bash
     git archive --format=tar.gz --prefix=csci6032-hw2-<github-username>/ \
       -o csci6032-hw2-<github-username>.tar.gz HEAD
     ```

   - Do not build the archive by taring the working directory, which would capture `.git`, caches, and untracked files.
   - List the contents and show them before any browser action:

     ```bash
     tar -tzf csci6032-hw2-<github-username>.tar.gz
     ```

   - Leave the archive untracked. Never stage or commit it; `.gitignore` excludes `*.tar.gz`.

6. Display the exact submission payload.
   - Report the exact notebook file to be submitted.
   - Report the exact archive file to be uploaded or attached.
   - Report the repository URL that will be included in Blackboard.
   - Report the exact submission text to be entered in Blackboard.
   - If the student has not reviewed and approved the final payload, stop.

## Browser and Blackboard safety rules

7. Ask before opening or controlling the Blackboard tab.
   - Before any browser operation, explain the action and ask for explicit permission.
   - Never open a browser tab or interact with Blackboard in the background without the student's approval.

8. Require personal authentication only.
   - Do not request, read, store, type, or expose credentials.
   - The student must authenticate to Blackboard personally in a browser session.
   - The skill must never ask for tokens, passwords, cookies, or device codes.

9. Navigate only to the homework submission page.
   - Use the existing authenticated Blackboard tab only for this assignment.
   - Do not browse unrelated pages, course content, or student portal pages.
   - If the target page is not available or the student is not authenticated, stop and instruct the student to complete that step.

10. Stage only the required files and repository URL.
   - Fill in the correct repository URL.
   - Attach or stage the required notebook and archive only.
   - Review the final fields before any irreversible action.

11. Stop immediately before the final submission action.
   - Present the exact final payload, including archive name, notebook, repository URL, and Blackboard text.
   - Show the student the exact action that would happen if they confirm.
   - Do not click the final submit button automatically unless the student has explicitly confirmed that exact payload.

12. Require explicit confirmation at that point.
   - A general prior approval is not sufficient.
   - The student must explicitly confirm the final submission action immediately before submission.
   - If there is any doubt, stop and return to the review step.

## Final submission and verification

13. After explicit confirmation, complete the final submission action, verify the receipt or confirmation page, and report the result.
   - Capture the confirmation page or receipt text only as needed to confirm success.
   - Do not store browser data, screenshots, or receipts in the repository.
   - If the automation cannot safely perform the final click, stop and ask the student to submit manually while explaining the limitation.

14. Do not commit Blackboard artifacts to the public repository.
   - Never add screenshots, receipts, browser data, cookies, session data, or personal information to commits.
   - Keep all Blackboard confirmation evidence out of version control and out of the repository.
   - Any browser or submission artifacts must remain local-only and be explicitly excluded from the public repo.

## Example operating flow

The host shell for this repository is PowerShell on Windows, so prefer Git commands
and `Get-ChildItem` over Unix-only utilities such as `ls -1`.

```bash
# 1) Preflight checks
git rev-parse --show-toplevel
git remote -v
git status --short
git log --oneline -n 10
git ls-files

# 2) Dry run (the default mode)
# Perform checks, build the archive from HEAD with git archive, list its contents,
# print archive file name, repo URL, notebook file, and final Blackboard text.
# Do not open Blackboard.

# 3) Only after student approval and authentication
# Navigate to the homework submission page and stage the required files.
# Display the exact final payload.
# Ask again for explicit confirmation just before final submit.

# 4) After final confirmation
# Complete the final submit.
# Read the confirmation page or receipt.
# Report the final result without committing any browser artifacts.
```

## Success criteria

The skill is successful only if:

- the repo is verified and safe,
- the branch is reviewed and pushed,
- the archive is prepared from the committed `HEAD`,
- the dry run is complete,
- the student personally authenticates,
- the final submission step is confirmed immediately before it happens,
- and the confirmation page is verified without storing Blackboard artifacts in the repository.
