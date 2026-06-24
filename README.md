# Every Corner Tees — Website

Custom t-shirt quote request site built with Flask + plain HTML/CSS.

---

## Project structure

```
everycornertees/
├── app.py              ← Flask backend
├── requirements.txt    ← Python packages
├── Procfile            ← Railway/gunicorn start command
├── templates/
│   └── index.html      ← Main page
├── static/
│   ├── css/style.css
│   └── js/main.js
└── uploads/            ← (gitignored, not used in production)
```

---

## Run locally (first time setup)

1. Make sure Python 3 is installed. Open a terminal in VS Code (`Ctrl + `` ` ``).

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate it:
   - Mac/Linux: `source venv/bin/activate`
   - Windows:   `venv\Scripts\activate`

4. Install packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the site:
   ```bash
   python app.py
   ```

6. Open your browser at http://localhost:5000

---

## Deploy to Railway

1. Create a free account at https://railway.app

2. Install Git if you haven't: https://git-scm.com

3. In your project folder, run:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

4. Push to GitHub:
   - Create a new repo at https://github.com/new (call it everycornertees)
   - Follow the "push existing repo" instructions GitHub shows you

5. In Railway:
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your everycornertees repo
   - Railway auto-detects Python and deploys it

6. Railway gives you a URL like `everycornertees.up.railway.app` — your site is live!

---

## Set up email (so form submissions reach you)

In Railway, go to your project → Variables → Add these:

| Variable   | Value                          |
|------------|-------------------------------|
| SMTP_HOST  | smtp.gmail.com                 |
| SMTP_PORT  | 587                            |
| SMTP_USER  | your.email@gmail.com           |
| SMTP_PASS  | (your Gmail App Password)      |
| TO_EMAIL   | hello@everycornertees.ca       |

**Gmail App Password setup:**
1. Go to myaccount.google.com → Security → 2-Step Verification (turn on)
2. Then go to myaccount.google.com/apppasswords
3. Create an app password for "Mail"
4. Paste that 16-character password as SMTP_PASS

---

## Point everycornertees.ca to Railway

1. In Railway: Settings → Domains → Add Custom Domain → type `everycornertees.ca`
2. Railway shows you a CNAME record (something like `xxx.railway.app`)
3. Log in to wherever you bought your domain (e.g. Namecheap, GoDaddy, Google Domains)
4. Find DNS settings and add:
   - Type: CNAME
   - Host: @ (or leave blank)
   - Value: the Railway CNAME they gave you
5. Wait 10–30 minutes for DNS to propagate — your site will be live at everycornertees.ca

---

## Update the site later

Just edit the files in VS Code, then:
```bash
git add .
git commit -m "describe what you changed"
git push
```
Railway auto-redeploys every time you push. Takes about 60 seconds.
