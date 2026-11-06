# Prompt to paste into the new chat

Start the new session on the repository `harshbatra01/video-agent-skills`, then paste this:

```text
You are continuing a video job that another Claude session started. Everything is in this repo on the branch research/metro-media-house (not main).

1. Run: git fetch origin research/metro-media-house && git checkout research/metro-media-house
   If that fails, tell me in one line and stop.
2. Read handoff/2026-11-06-son-01/START-HERE.md fully. Then read jobs/son-01/HANDOFF.md, jobs/son-01/DADDY.md, jobs/son-01/script/DRAFT-v3.md and research/metro-media-house/STUDY.md sections 1, 5, 6 and 7.
3. Don't redo any finished work.
4. Follow my decisions and working style in START-HERE.md section 5 exactly: step by step with my approval, plain English, no em dashes, never fabricate, install nothing without asking, push only to research/metro-media-house.
5. Then reply with:
   - a summary in 10 lines of what we're making and where we are;
   - the open questions from START-HERE.md section 7, each with its default;
   - a quick test of which sites this environment can reach (YouTube, CNBC, Bloomberg, Instagram), using only allowed tools and without working around any block.
6. Wait for my go. The next phase is building the reel a few seconds at a time, starting with the hook.
```
