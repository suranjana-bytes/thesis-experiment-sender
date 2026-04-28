# Sender Experiment oTree App

This workspace contains a minimal oTree project for the sender experiment.

## Open in VS Code

Open this folder in VS Code:

`/Users/scribblonomics/Documents/Thesis Experiment`

## Recommended setup

1. Create a virtual environment:
   `python3 -m venv .venv`
2. Activate it:
   `source .venv/bin/activate`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Start oTree:
   `otree devserver`
5. Open the local URL shown in the terminal.

## What the app does

- Round 1 begins with a six-screen instruction section.
- Round 1 then shows 5 Raven matrix trials.
- Participants with odd `id_in_session` get Set 1: `Q2, Q8, Q11, Q12, Q15`.
- Participants with even `id_in_session` get Set 2: `Q17, Q18, Q24, Q26, Q30`.
- Raven score `> 2` gives `High Status`; Raven score `<= 2` gives `Low Status`.
- In every round, the participant receives a random type from 1 to 3.
- The participant chooses one or more messages.
- The app shows confirmation, round-finished, next-round, and final end screens across 10 rounds.

## Raven image files

Place the Raven images under `_static/raven/` using this structure:

- `_static/raven/Q2/matrix.png`
- `_static/raven/Q2/R1.png` through `_static/raven/Q2/R8.png`

Repeat that pattern for:

- `Q8`
- `Q11`
- `Q12`
- `Q15`
- `Q17`
- `Q18`
- `Q24`
- `Q26`
- `Q30`

## Main files

- `settings.py`
- `sender_experiment/__init__.py`
- `sender_experiment/templates/sender_experiment/`
