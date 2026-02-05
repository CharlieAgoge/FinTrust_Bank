# FinTrust Bank

Update

**Your first app on the Cyber Agoge Bootcamp.** FinTrust Bank is a secure-by-design banking web app you’ll clone, run locally, and log into in Lesson 1—then use throughout the 6-week programme to learn the CIA triad, login flows, and DevSecOps. Follow the **Gamma** deck your instructor shares for step-by-step direction in class.

---

## Lesson 1: Your first steps Hello how are you 

Do these in order. By the end you’ll have the app running and you’ll be logged in.

### 1. Clone the repo

```bash
git clone https://github.com/CharlieAgoge/FinTrust_Bank.git
cd FinTrust_Bank
```

### 2. Install Cursor

If you don’t have it yet:

- Go to **[cursor.com](https://cursor.com)** and download Cursor (the code editor we use on the bootcamp).
- Install it and open Cursor.

### 3. Open the project in Cursor

- In Cursor: **File → Open Folder** (or **Open…** on Mac).
- Choose the `FinTrust_Bank` folder you just cloned.
- You should see the project files in the sidebar.

### 4. Run the app

Open the terminal in Cursor (**Terminal → New Terminal** or `` Ctrl+` `` / `` Cmd+` ``), then run:

**On Mac / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.app:app
flask run
```

**On Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FLASK_APP="app.app:app"
flask run
```

You should see something like: **Running on http://127.0.0.1:5000**

### 5. Log in

1. Open your browser and go to: **http://127.0.0.1:5000**
2. Click **Log in** (or go straight to **http://127.0.0.1:5000/login**).
3. Use the demo account:
   - **Username:** `student`
   - **Password:** `demopassword`
4. You’re in. You should see your dashboard with balance and transfer—that’s your first successful run.

---

## What you just did

You used **Git** (clone), **Cursor** (editor), and **Python/Flask** (run the app). In the next lessons you’ll add **Docker**, map the **CIA triad** to this app, and start thinking like a defender.

## Run with Docker (later)

When you’re ready for containers:

```bash
cd FinTrust_Bank
docker compose up --build
```

Then open **http://localhost:5000** and log in with `student` / `demopassword`.

## Teaching and Module 1

- **[docs/LESSON1.md](docs/LESSON1.md)** — One-page “Lesson 1” handout (clone → Cursor → run → log in).
- **[docs/MODULE1_TIEIN.md](docs/MODULE1_TIEIN.md)** — CIA triad in the app, attack surface, and Week 3+ ideas.

## Tech

- **Backend:** Python 3.11, Flask  
- **Data:** SQLite in `instance/` (no extra DB setup)  
- **Containers:** `Dockerfile` + `docker-compose.yml` for one-service run
