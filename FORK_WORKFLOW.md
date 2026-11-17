# Personal fork workflow

`master` is the stock llama.cpp source of truth. Keep it close to upstream. Open Agents uses a small chat adapter in its own repository; do not copy the llama.cpp source tree into that adapter or this fork.

Make each proposed fix in a named `review/<topic>` branch. Keep unverified ideas in `experiment/<topic>` branches. Record the upstream base commit, build commit, test command, and result with the branch or its review request. A model/runtime experiment must not silently change the Open Agents production binary or profile.

Promote a change only after its relevant regression test passes and its diff is reviewed against the current upstream base. Keep discarded experiments in Git history, not in parallel `source-copy`, `backup`, or `snapshot` directories. Use the existing upstream tests and tools; add a focused regression only for behavior changed by the fix.

The fork boundary check runs on pull requests. It rejects generated runtime/model files, machine-specific paths, and copied source trees in changed files. Run it locally with `python scripts/check_fork_boundaries.py --base master` before opening a review request.
