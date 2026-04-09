# Emotional Support Chatbot

A small Python project that guides users through a **structured emotional check-in**, guesses a primary emotion with **keyword-based NLP**, and responds with **empathy**, **coping ideas**, a **suggested exercise** (breathing, grounding, journaling, affirmations), and a **~5-minute action plan**.

**Important:** This is a self-help support tool. It is **not** therapy, medical advice, or a crisis service. If you are in danger or feel unsafe, contact local emergency services or a crisis helpline in your area.

## Requirements

- **Python 3.8+** (uses `from __future__ import annotations`)
- **Tkinter** (included with most official Windows/macOS Python installers; on some Linux distributions install `python3-tk`)

No third-party packages are required.

## Project structure

| File | Description |
|------|-------------|
| `emotional_support_chatbot.py` | Core logic: emotion data, detection, responses, exercises, action plan, and **CLI** loop |
| `emotional_support_gui.py` | **Tkinter** GUI; imports logic from the chatbot module |

## How to run

From the project folder:

**Command-line chatbot**

```bash
python emotional_support_chatbot.py
```

Type answers at the prompts. Type `quit` at any prompt (or at the “another check-in” step) to exit.

**Graphical interface**

```bash
python emotional_support_gui.py
```

Use **Start check-in**, answer each step, then **See support**. **New check-in** clears the form for another round.

### Windows console encoding (optional)

If punctuation or symbols look wrong in the CLI, you can force UTF-8 for that session:

```powershell
$env:PYTHONIOENCODING='utf-8'
python emotional_support_chatbot.py
```

## Supported emotion categories

Detection is **keyword-based** (with whole-word matching for single-word cues to limit false positives). Categories:

- Anxiety  
- Stress  
- Sadness  
- Anger  
- Loneliness  
- Happiness  

If nothing matches strongly, the bot treats the mood as **neutral** and still offers gentle, generic support.

## What the bot does

1. Asks how you feel today and follows with short structured questions (emotions, cause/context, intensity 1–10, duration).  
2. Combines your text to infer a **primary** emotion.  
3. Outputs a **supportive summary**, **practical suggestion**, optional **intensity-based** note (e.g. encouragement to seek professional help at high intensity), plus a **motivational** line.  
4. Suggests one **random** exercise from that emotion’s library (breathing, 5-4-3-2-1 grounding, journaling, affirmations).  
5. Prints a **5-minute action plan** with simple timed steps.

## Extending the project

- Add or edit keywords and copy in the `EMOTION_DATA` dictionary in `emotional_support_chatbot.py`.  
- For heavier NLP or ML later, you could replace or augment `detect_emotion()` while keeping the same response dictionaries.

## Publish to GitHub

### 1. Install Git (if `git` is not recognized)

- Download **Git for Windows**: [https://git-scm.com/download/win](https://git-scm.com/download/win)  
- Run the installer; keep the default that adds Git to your **PATH**.  
- **Close and reopen** PowerShell or Cursor’s terminal so `git` works.

Check:

```powershell
git --version
```

### 2. Create an empty repository on GitHub

1. Sign in at [https://github.com](https://github.com).  
2. Click **+** → **New repository**.  
3. Choose a name (e.g. `emotional-support-chatbot`).  
4. Leave it **empty**: no README, no `.gitignore`, no license (this project already has them).  
5. Click **Create repository**. GitHub will show you a URL like  
   `https://github.com/YOUR_USERNAME/emotional-support-chatbot.git`

### 3. Initialize Git in this folder and push

In PowerShell (replace `YOUR_USERNAME` and `REPO_NAME` with yours):

```powershell
cd C:\Users\pavilion\Desktop\HEXTASK1

git init
git branch -M main
git add README.md .gitignore emotional_support_chatbot.py emotional_support_gui.py
git commit -m "Initial commit: emotional support chatbot CLI and GUI"

git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git push -u origin main
```

The first `git push` may open a **browser or credential** prompt to sign in to GitHub. If GitHub disables password pushes, use a **Personal Access Token** as the password, or install [GitHub CLI](https://cli.github.com/) and run `gh auth login`.

### Optional: GitHub CLI

If you use `gh` and are logged in:

```powershell
cd C:\Users\pavilion\Desktop\HEXTASK1
git init
git branch -M main
git add .
git commit -m "Initial commit: emotional support chatbot CLI and GUI"
gh repo create emotional-support-chatbot --public --source=. --remote=origin --push
```

Adjust `--public` to `--private` if you want the repo private.

## License

Use and modify freely for learning or personal projects; add a license file if you redistribute.
