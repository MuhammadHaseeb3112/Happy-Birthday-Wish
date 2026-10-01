# Jaan_Birthday: run & deploy

## Local run (Windows, from the project folder)
```
.venv\Scripts\activate
pip install -r requirements.txt        <-- this fixes "No module named 'whitenoise'"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Admin: http://127.0.0.1:8000/admin/ → Photos → upload pictures + captions.

Frontend: open `frontend/index.html` with VS Code Live Server (port 5500) and set in CONFIG:
`apiUrl: "http://127.0.0.1:8000"`. Add `?test=1` to the URL to skip the countdown.

## Before deploying
- `.env`: new SECRET_KEY, real BIRTHDAY_PASSWORD, DEBUG=0 (use .env.example as a guide, or host env vars)
- `frontend/index.html`: `allowTest:false`, `apiUrl:"https://<your-backend>"`
- `python manage.py collectstatic --noinput`
- Host photos somewhere that keeps files (PythonAnywhere / Cloudinary), then test on your phone.
