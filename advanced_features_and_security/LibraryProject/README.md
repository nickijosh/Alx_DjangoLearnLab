# LibraryProject

This is a basic Django project setup for the ALX Introduction to Django task.

## Project Structure

- `manage.py`: Django’s command-line utility.
- `LibraryProject/settings.py`: Project configuration.
- `README.md`: This file confirms project setup.

## Setup Instructions

1. Clone the repo
2. Navigate into the folder
3. Run the development server:

```bash
python manage.py runserver
This confirms the setup is complete.
happy

## HTTPS and Security Configuration

The Django application has been secured using the following techniques:

### 1. HTTPS Enforcement
- `SECURE_SSL_REDIRECT = True` ensures all HTTP requests are redirected to HTTPS.
- Nginx is configured with SSL certificates using Let's Encrypt.

### 2. Secure Cookies
- `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` ensure cookies are only sent over HTTPS.

### 3. HTTP Headers
- `X_FRAME_OPTIONS = "DENY"` blocks clickjacking.
- `SECURE_CONTENT_TYPE_NOSNIFF = True` prevents MIME-type sniffing.
- `SECURE_BROWSER_XSS_FILTER = True` enables browser XSS filter.

### 4. HSTS (HTTP Strict Transport Security)
- Configured to 1 year with preload and subdomain protection.

### 5. Deployment Notes
- Nginx redirects HTTP to HTTPS and proxies to the Django app on port 8000.
- SSL certificate is configured at `/etc/ssl/certs/your-cert.pem`.

**All settings are located in** `LibraryProject/settings.py`.

