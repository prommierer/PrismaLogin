import os

# geheimes Schlüsselwort für Sessions
SECRET_KEY = os.environ.get("SECRET_KEY")  # PLACEHOLDER: z.B. prisma_super_secret_123

# Email Einstellungen (für Bestätigung & Passwort Reset)
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")  # PLACEHOLDER: DEINE Gmail
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")  # PLACEHOLDER: Gmail App Passwort

# reCAPTCHA
RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY")  # PLACEHOLDER: Google reCAPTCHA Site Key
RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY") # PLACEHOLDER: Google reCAPTCHA Secret Key