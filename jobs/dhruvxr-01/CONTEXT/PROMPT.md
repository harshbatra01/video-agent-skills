# Prompt to paste into the new chat

You're continuing a video job started in another chat. Everything is in the GitHub repo harshbatra01/video-agent-skills, on branch `job/dhruvxr`.

1. Get the branch: `git fetch origin job/dhruvxr && git checkout job/dhruvxr`.
2. Read `jobs/dhruvxr-01/CONTEXT/CONTEXT.md` in full first. It has my working rules, what's done, the latest numbers, the open items and how to run the build. Then read `jobs/dhruvxr-01/DIRECTION_v1.md` and `jobs/dhruvxr-01/HANDOFF.md`.
3. Skim `research/dhruvxr/STUDY.md` and `skills/video-agent/SKILL.md` and `skills/edit-loop-guard/SKILL.md` so you know the method.
4. Check that you can run the build: Python 3 with numpy and Pillow, ffmpeg, and the Inter font. Fix the font paths at the top of `jobs/dhruvxr-01/build/build.py` if needed. Install nothing without telling me the name, source and size first.
5. Then reply with: a short summary of where the job stands in your own words, anything in the files that looks inconsistent, and the next step you propose. Wait for my approval before building.

Rules: plain English, short points, exact numbers, no em dashes. Never fabricate. Say what you measured, what you judged, and what you didn't check. Show every report in the chat. Work on `job/dhruvxr` and commit and push after each step. Never push to main.
