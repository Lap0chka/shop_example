🛒 Online Store (Django-based)

A fully featured e-commerce web application built using Django 5.2.5, REST API, Celery, Stripe integration, admin tools, and more.

⸻

🚀 Features
	•	🧑‍💻 JWT-based authentication using Djoser + SimpleJWT
	•	✅ Email verification
	•	🔐 Social login (OAuth)
	•	📦 Product and order management via REST API
	•	💸 Stripe payment integration
	•	📄 PDF generation with WeasyPrint
	•	📧 Email notifications
	•	🖼 Image caching with sorl-thumbnail
	•	⏱ Background tasks with Celery
	•	⏲ Periodic tasks with django-celery-beat
	•	📐 Admin UI with crispy-bootstrap5
	•	🌐 Google Fonts integration
	•	⚡ HTMX support
	•	📚 Interactive API docs via Swagger (drf-yasg)

⸻

🐞 Django Debug Toolbar

The Django Debug Toolbar is used to inspect database queries, cache, signals, and more — a must-have for debugging during development.

⸻

🕓 Django Simple History

Django Simple History tracks changes to model instances over time.

🔍 Why Use It
	•	🔒 Auditing — who changed what and when
	•	🧪 Debugging — inspect previous values
	•	⏪ Recovery — revert to earlier states if needed

🧱 Example Model

from django.db import models
from simple_history.models import HistoricalRecords

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    history = HistoricalRecords()

🛠 Migrations

python manage.py makemigrations
python manage.py migrate

🧪 Usage Example

product = Product.objects.create(name="Phone", price=500)
product.price = 450
product.save()

for record in product.history.all():
    print(record.history_date, record.price)

🖥 Admin Integration

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Product

admin.site.register(Product, SimpleHistoryAdmin)


⸻

🔐 Security Best Practices

1. 🌐 django-cors-headers

Configure CORS to restrict API access to trusted domains.

2. 🧱 Secure Headers in Django

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

These settings protect your site from XSS, MIME sniffing, clickjacking, and enforce HTTPS.

3. 🔐 django-csp

Content Security Policy (CSP) restricts allowed sources for scripts, styles, and media to prevent XSS and data injection.

⸻

🛠 Adminer in Docker

Adminer is a lightweight alternative to phpMyAdmin, available via Docker.

🐳 Quick Start

docker-compose up -d

Adminer will be available at http://localhost:8080

🔐 Connection Info
	•	System: PostgreSQL / MySQL
	•	Server: name of your DB service (e.g. db)
	•	Username / Password: from your Django settings
	•	Database: your actual database name

⸻

🧪 Code Quality Tools

The project uses several tools for maintaining code quality:

Category	Tool	Purpose
Formatting	black	Auto-formatting of Python code
Typing	mypy	Static type checking
Style Guide	flake8	PEP8 compliance and linting
Code Analysis	pylint	Deep static analysis and code quality

These tools are integrated via scripts and CI pipelines for consistency and reliability.

⸻

🔓 Open Source

This project is completely open source and available for contribution, learning, or use in your own applications.

Feel free to fork, star, and contribute!

⸻

Let me know if you want a Docker setup, .env template, or CI configuration included too.