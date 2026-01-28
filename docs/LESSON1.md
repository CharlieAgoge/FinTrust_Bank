# Lesson 1: Clone, open in Cursor, run, log in

Use this as a handout or slide for the first lesson. Students do each step in order. **In class:** use the Gamma deck for direction; this doc is the written reference.

---

## Step 1 — Clone the repo

```bash
git clone https://github.com/CharlieAgoge/FinTrust_Bank.git
cd FinTrust_Bank
```

---

## Step 2 — Install Cursor

- Go to **[cursor.com](https://cursor.com)** and download Cursor.
- Install and open it.

---

## Step 3 — Open the project in Cursor

- **File → Open Folder** → select the `FinTrust_Bank` folder.
- Confirm you see the project in the sidebar.

---

## Step 4 — Run the app

Open the terminal in Cursor (**Terminal → New Terminal** or `` Ctrl+` `` / `` Cmd+` ``).

**Mac / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.app:app
flask run
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FLASK_APP="app.app:app"
flask run
```

Look for: **Running on http://127.0.0.1:5000**

---

## Step 5 — Log in

1. In your browser, open **http://127.0.0.1:5000**
2. Click **Log in**
3. Use:
   - **Username:** `student`
   - **Password:** `demopassword`
4. You should see the FinTrust Bank dashboard (balance and transfer). **You’re done.**

---

## Success checklist

- [ ] Repo cloned  
- [ ] Cursor installed and project opened  
- [ ] App running (`flask run` with no errors)  
- [ ] Logged in at http://127.0.0.1:5000 with `student` / `demopassword`  
- [ ] Dashboard visible  

**In class:** Your instructor will share a Gamma deck with the lesson flow. Use this doc as a written reference or if you’re catching up.

Next: we’ll map the CIA triad to this app and run it in Docker.
