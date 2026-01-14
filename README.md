🚀 Django SaaS Boilerplate

A production-grade, multi-tenant SaaS backend built with Django & Django REST Framework.

This project implements the same backend architecture used by real SaaS companies like Stripe, Notion, and OpenAI — including authentication, organizations, teams, subscriptions, billing limits, and API-key based access.

❌ Not a demo app
✅ This is how real SaaS backends are engineered.

🌟 What This Project Demonstrates

Most Django projects show:

Login → CRUD → Logout ❌

This project shows:

How a real SaaS product is built from the backend up ✅

It includes:

Multi-tenant architecture

Subscription enforcement

Team & role management

API-key based SaaS access

Backend-level paywalls

🧩 Core Features
🔐 Authentication & Security

Custom email-based User model

JWT authentication (access & refresh tokens)

Email verification

Token-based security everywhere

🏢 Organizations (Multi-Tenant)

Users can create multiple organizations

Each organization has:

Owner

Admins

Members

Secure invitation system using tokenized invite links

💳 Subscriptions & Billing

Built-in SaaS plans:

Free

Pro

Business

Each plan controls:

Maximum team members

Monthly API usage

Organizations must subscribe before using the platform.
Plan upgrades are supported.

🔐 SaaS Paywall (Very Important)

The backend strictly enforces monetization:

Team size limited by plan

Pending invites count toward limits

When limits are reached:

New invites are blocked

This logic runs on the server, not the frontend.
It cannot be bypassed — this is how real SaaS companies prevent revenue leaks.

🔑 API Keys (Stripe-Style)

Organizations can generate API keys like:

sk_live_xxxxxxxxxxxxxxxxx


These keys:

Identify the organization

Are used by external apps to access the SaaS

Work just like Stripe / OpenAI API keys

📡 API-Key Protected SaaS APIs

SaaS endpoints are protected by API keys, not JWTs.

This allows:

External clients

Mobile apps

Other services

to securely use your SaaS.

🧱 Tech Stack

Django

Django REST Framework

SimpleJWT

Token-based authentication

SQLite (can be replaced with PostgreSQL)

Clean multi-tenant backend architecture

🗺️ System Architecture
User
 └── Membership
      └── Organization
            ├── Subscription → Plan
            └── API Keys


One user → many organizations

One organization → one active subscription

One plan → controls SaaS limits

This is the same architecture used by real SaaS startups.

🔌 Complete SaaS API Flow

1️⃣ Signup & verify email
POST /api/signup/

2️⃣ Login (JWT)
POST /api/token/

3️⃣ Create organization
POST /api/orgs/create/

4️⃣ Subscribe to plan
POST /api/billing/<org_id>/subscribe/

5️⃣ Invite team members
POST /api/orgs/<org_id>/invite/

6️⃣ Generate API key
POST /api/orgs/<org_id>/keys/

7️⃣ Use SaaS API
GET /api/saas/data/
Authorization: Bearer sk_live_xxxxx

🔌 Example API Usage
🔑 Login
POST /api/token/
{
  "email": "user@gmail.com",
  "password": "password"
}

🏢 Create Organization
POST /api/orgs/create/
Authorization: Bearer <JWT>

👥 Invite Team Member
POST /api/orgs/1/invite/
Authorization: Bearer <JWT>

🔐 Generate API Key
POST /api/orgs/1/keys/
Authorization: Bearer <JWT>

📡 Call SaaS API
GET /api/saas/data/
Authorization: Bearer sk_live_xxxxx

📂 Project Structure
accounts/       → User accounts & authentication  
organizations/ → Organizations, members, invites  
billing/       → Plans, subscriptions, upgrades  
api_keys/      → API key system  
webhooks/      → SaaS integrations  

💼 Why This Project Stands Out

Most portfolios show:

Blog apps, todo lists, CRUD dashboards ❌

This project shows:

✔ Real SaaS architecture
✔ Multi-tenant backend
✔ Subscription-based paywalls
✔ API-key security
✔ Team & role management
✔ Monetization-ready design

This is how actual startup backends are built.

## 🛠️ Local Setup

```bash
git clone https://github.com/yourusername/django-saas-boilerplate.git
cd django-saas-boilerplate

python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt

copy .env.example .env

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Now open:
http://127.0.0.1:8000

```markdown
![Django](https://img.shields.io/badge/Django-5.x-green)
![DRF](https://img.shields.io/badge/DRF-API-blue)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![SaaS](https://img.shields.io/badge/Type-SaaS-purple)

👨‍💻 Author

Rohit Kiroriwal
Python • Django • SaaS Backend Engineer 🚀