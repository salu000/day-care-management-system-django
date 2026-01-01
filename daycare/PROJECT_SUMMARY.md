# Day-Care Management System - Project Summary

## Project Overview
A Django-based web application for managing day-care operations including student enrollment, staff management, attendance tracking, billing, and events.

**Tech Stack:**
- **Framework:** Django 5.2.8
- **Database:** SQLite3 (db.sqlite3)
- **Python Version:** 3.x
- **Frontend:** Bootstrap, HTML/CSS, JavaScript
- **PDF Generation:** WeasyPrint, ReportLab, xhtml2pdf
- **Image Processing:** Pillow 12.0.0

---

## Core Dependencies
```
Django==5.2.8
Pillow==12.0.0                    # Image handling
psycopg2-binary==2.9.11          # PostgreSQL (optional)
WeasyPrint==67.0                  # PDF generation
reportlab==4.4.5                  # PDF reports
xhtml2pdf==0.2.17                 # HTML to PDF
requests==2.32.5
```

---

## Project Structure & Installed Apps

```
daycare/                          # Main project folder
├── daycare/                      # Project settings
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Main URL routing
│   ├── wsgi.py                  # WSGI config
│   └── asgi.py                  # ASGI config
│
├── children/                     # Student Management App
├── staff/                        # Staff Management App
├── guardians/                    # Guardian/Parent Management App
├── attendance/                   # Attendance Tracking App
├── billings/                     # Invoice & Billing App
├── events/                       # Events Management App
├── dashboard/                    # Dashboard/Analytics App
├── users/                        # Authentication & User Management
│
├── templates/                    # HTML templates (all apps)
├── static/                       # CSS, JS, Images
├── media/                        # User uploaded files
├── db.sqlite3                    # SQLite Database
└── manage.py                     # Django management
```

---

## Database Schema & Models

### 1. **CHILDREN APP** - Student/Child Management
**Model: Child**
```python
Fields:
- id (Auto PK)
- guardian (FK → Guardian)
- full_name (CharField, max_length=100)
- dob (DateField) - Date of Birth
- gender (CharField) - Choices: Male, Female, Other
- enrollment_class (CharField) - Choices: Infants, Toddlers, Pre-K
- start_date (DateField, default=now)
- photo (ImageField, upload_to='children/', optional)
- status (CharField) - Choices: Active, Pending, Left
- default_daily_rate (DecimalField) - Default daily charge
- created_at (Auto)
- updated_at (Auto)

Methods:
- get_student_id(): Returns formatted ID like #1001
```

**Relationships:**
- One Guardian has many Children (1:N)
- Child has many Attendance records (1:N)
- Child has many Invoices (1:N)

---

### 2. **GUARDIANS APP** - Parent/Guardian Management
**Model: Guardian**
```python
Fields:
- id (Auto PK)
- name (CharField, max_length=100)
- phone (CharField, max_length=20)
- email (EmailField)
- address (TextField)
- photo (ImageField, upload_to='guardians/', optional)
- created_at (DateTimeField, auto_now_add=True)

Methods:
- __str__(): Returns name
```

**Relationships:**
- One Guardian has many Children (1:N)

---

### 3. **STAFF APP** - Staff Management
**Model: StaffMember**
```python
Fields:
- id (Auto PK)

PERSONAL DETAILS:
- first_name (CharField, max_length=100)
- last_name (CharField, max_length=100)
- father_spouse_name (CharField, max_length=100)
- gender (CharField) - Choices: M, F, O
- photo (ImageField, upload_to='staff_photos/', optional)
- date_of_birth (DateField, optional)

CONTACT DETAILS:
- email (EmailField, unique=True)
- phone (CharField, max_length=15)
- address (TextField)

JOB DETAILS:
- role (CharField) - Choices: Teacher, Assistant, Admin, Cleaner, Driver, Security
- date_joined (DateField, default=now)
- salary (DecimalField) - Monthly salary
- status (CharField) - Choices: Active, On Leave, Resigned

Methods:
- __str__(): Returns "FirstName LastName"
- full_name (property): Returns full name
```

---

### 4. **ATTENDANCE APP** - Attendance Tracking
**Model: Attendance**
```python
Fields:
- id (Auto PK)
- child (FK → Child, cascade)
- date (DateField, default=now)
- status (CharField) - Choices: ABSENT, PRESENT, LEAVE
- check_in_time (TimeField, optional)
- check_out_time (TimeField, optional)
- created_at (DateTimeField, auto_now_add=True)
- updated_at (DateTimeField, auto_now=True)

Constraints:
- unique_together: (child, date) - One record per child per day
- ordering: ['child']

Methods:
- __str__(): Returns "ChildName - Date - Status"
```

**Relationships:**
- Child has many Attendance records (1:N)

---

### 5. **BILLINGS APP** - Invoicing & Billing Management
**Model: Invoice**
```python
Fields:
- id (Auto PK)
- child (FK → Child, cascade)

DATES:
- created_at (DateTimeField, auto_now_add=True)
- due_date (DateField)
- period_start (DateField) - Billing period start
- period_end (DateField) - Billing period end

CALCULATION DATA:
- total_days_present (IntegerField, default=0)
- daily_rate_applied (DecimalField)

FINANCIALS:
- base_amount (DecimalField) - Days * Rate
- adjustment_amount (DecimalField, default=0) - Extra charge or discount
- adjustment_reason (CharField, optional)
- total_amount (DecimalField) - Auto-calculated
- amount_paid (DecimalField, default=0)
- status (CharField) - Choices: UNPAID, PARTIAL, PAID

Methods:
- save(): Auto-calculates total_amount and updates status
- get_balance_due(): Returns outstanding amount
- __str__(): Returns "INV-{id} - {ChildName}"
```

**Relationships:**
- Child has many Invoices (1:N)

---

### 6. **USERS APP** - Authentication
**Model:** Uses Django's built-in User model (django.contrib.auth)
- For user login and authentication

---

### 7. **EVENTS APP** - Events Management
**Model:** Empty (currently no custom models)
- For managing day-care events

---

### 8. **DASHBOARD APP** - Analytics/Dashboard
**Model:** Empty (currently no custom models)
- For displaying summary data and analytics

---

## Database Relationships Diagram

```
Guardian (1) ←→ (N) Child
                  ├── (1) ←→ (N) Attendance
                  └── (1) ←→ (N) Invoice

Staff (Independent)

User (Built-in Django model)
```

---

## URL Routing

```
/ or /login/              → users.urls (Login/Logout/Index)
/admin/                   → Django Admin
/dashboard/               → dashboard.urls
/staff/                   → staff.urls (CRUD operations)
/children/                → children.urls (Student management)
/guardians/               → guardians.urls (Parent management)
/billing/                 → billings.urls (Invoices)
/attendance/              → attendance.urls (Attendance tracking)
/events/                  → events.urls (Events)
```

---

## Key Views & Functionality

### USERS MODULE
- `Index()` - Home page
- `Login()` - User authentication
- `Logout()` - Logout user
- `users_list()` - List system users

### STAFF MODULE
- `staff_list()` - Display all staff
- `staff_create()` - Add new staff member
- `staff_update()` - Edit staff details
- `staff_delete()` - Remove staff

### CHILDREN MODULE
- `admission_form()` - New student enrollment
- `all_students()` - Display all students
- `student_detail_ajax()` - Student details (AJAX)
- `student_delete()` - Remove student
- `student_promotion()` - Promote to next class
- `class_list()` - List by class

### GUARDIANS MODULE
- `guardian_list()` - Display all guardians
- `guardian_detail_ajax()` - Guardian details (AJAX)
- `guardian_delete()` - Remove guardian

### ATTENDANCE MODULE
- Daily attendance tracking
- Check-in/Check-out times

### BILLINGS MODULE
- `billing_view()` - View invoices
- `generate_invoice()` - Create new invoice
- Invoice generation with PDF export

### DASHBOARD MODULE
- `dashboard_index()` - Summary statistics

### EVENTS MODULE
- `dashboard_index()` - Events dashboard

---

## Media Storage

**Upload Directories:**
- `/media/children/` - Child photos
- `/media/guardians/` - Guardian photos
- `/media/staff_photos/` - Staff photos
- `/media/staff/` - Staff documents

---

## Static Files

**Static Directories:**
- `/static/css/` - Bootstrap and custom CSS
- `/static/js/` - Bootstrap JavaScript
- `/static/images/` - Logo and images

---

## Settings Configuration

**Key Settings:**
- `DEBUG = True` (Development)
- `ALLOWED_HOSTS = []` (Update for production)
- `SECRET_KEY = 'django-insecure-...'` (Change for production)
- `DATABASES`: SQLite3 (can switch to PostgreSQL)
- `LOGIN_URL = '/login/'`
- `LOGIN_REDIRECT_URL = '/'`
- `MEDIA_URL = '/media/'`
- `STATIC_URL = '/static/'`

---

## Authentication & Security

- Uses Django's built-in authentication system
- Login required for most views
- CSRF protection enabled
- Session middleware enabled
- No custom permission system currently implemented

---

## Template Structure

```
templates/
├── base.html              - Base template
├── error.html             - Error page
├── login.html             - Login form
├── attendance/
│   └── daily_tracker.html
├── billings/
│   ├── billing_view.html
│   └── invoice_pdf.html
├── children/
│   ├── admission_form.html
│   ├── all_students.html
│   └── partials/
│       └── student_edit_modal.html
├── dashboard/
│   └── index.html
├── events/
│   └── dashboard_index.html
├── guardians/
│   ├── guardian_list.html
│   └── partials/
│       └── guardian_edit_modal.html
├── staff/
│   ├── staff_list.html
│   └── partials/
│       └── staff_form_modal.html
└── users/
    └── users_list.html
```

---

## Current Features

✅ Student/Child Management (CRUD)
✅ Guardian/Parent Management (CRUD)
✅ Staff Management (CRUD)
✅ Attendance Tracking (Check-in/Out)
✅ Invoice Generation & Billing
✅ Dashboard/Analytics
✅ User Authentication & Login
✅ PDF Invoice Export
✅ Modal-based AJAX Forms
✅ Photo Upload (Students, Staff, Guardians)

---

## Areas Ready for New Module Integration

1. **Event Management** (events app) - Currently empty, can add event details, attendees, etc.
2. **Analytics/Reports** (dashboard app) - Can add custom reports
3. **Notifications** - Email or SMS alerts
4. **Health & Medical Records** - Track vaccinations, medical history
5. **Parent Portal** - Allow parents to view attendance, invoices
6. **Meal Plans/Nutrition** - Track meals and dietary requirements
7. **Payments Gateway** - Online payment integration
8. **Activities/Curriculum** - Track learning activities and progress

---

## Database Constraints & Validations

**Child Model:**
- Guardian is required (FK)
- Email validation on Guardian

**Attendance Model:**
- Unique constraint: Cannot have duplicate attendance for same child on same date
- Date defaults to current date

**Invoice Model:**
- Auto-calculates total and status on save
- Child is required (FK)
- Amount paid cannot exceed total

**Staff Model:**
- Email must be unique
- Phone and address are required

---

## File Uploads

- Images stored in `/media/` directory
- Supported formats: JPG, PNG
- Upload paths: children/, guardians/, staff_photos/

---

## Notes for Development

1. **Database:** Currently using SQLite3. For production, migrate to PostgreSQL (psycopg2 already in requirements)
2. **Security:** Update SECRET_KEY and set DEBUG=False for production
3. **Email:** Configure email backend for notifications
4. **Static Files:** Run `python manage.py collectstatic` before deployment
5. **Migrations:** Run `python manage.py migrate` after model changes
6. **Forms:** Custom forms exist for Children and Staff in `forms.py` files
7. **Admin:** Custom admin configurations available in `admin.py` files

---

*Last Updated: January 1, 2026*
