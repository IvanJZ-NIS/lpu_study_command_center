# LPU Cavite Student Academic Command Center & Planner

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    python app.py          # then open http://127.0.0.1:5000

- Data lives in `database/command_center.db` (SQLite, created automatically). `database/mysql.sql` is the MySQL equivalent.
- Sign-up requires a `@lpu.edu.ph` email. For local testing, run with `CC_EMAIL_DOMAIN=` (empty) to allow any email.
- Forgot password: no mail server is configured, so the reset code is printed in the terminal (and auto-filled in debug mode).
- Set `CC_SECRET` to a fixed value in production so logins survive restarts.
- `python command_center_service.py` still runs the original OOP service-layer demo.
