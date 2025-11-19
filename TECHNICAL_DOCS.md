# SHINE Technical Documentation

## Overview

Django 4.1.7 web application for grading companies on human trafficking prevention training programs. Uses SQLite database and class-based views.

## Project Structure

```
traffickingGrader/     # Main Django project config
├── settings.py        # App config, database, templates
├── urls.py            # Root URL routing
└── wsgi.py

home/                  # Landing page app
├── views.py           # HomeView, AuthorizedView
└── templates/home/

companies/             # Company data management
├── models.py          # Companies, Language models
├── views.py           # CompanyListView, CompanyDetailView
└── templates/companies/

grading/               # (CURRENTLY NOT DEVELOPED) Grading criteria display
├── views.py           # GradingView
└── templates/grading/

about/                 # About page
├── views.py           # AboutView
└── templates/about/

apply/                 # Application page
├── views.py           # ApplyView
└── templates/apply/

static/                # Static assets
├── templates/base.html
└── images/, css/
```

## URL Routes

| Path            | App       | View              | Description      |
| --------------- | --------- | ----------------- | ---------------- |
| `/`           | home      | HomeView          | Landing page     |
| `/admin/`     | Django    | Admin             | Admin interface  |
| `/comp/`      | companies | CompanyListView   | Company listings |
| `/comp/<pk>/` | companies | CompanyDetailView | Company detail   |
| `/about/`     | about     | AboutView         | About page       |
| `/apply/`     | apply     | ApplyView         | Application page |
| `/grading/`   | grading   | GradingView       | Grading criteria |

## Data Models

### Companies (`companies/models.py`)

```python
class Companies:
    title          # CharField(100) - Company name
    about          # TextField - Company description
    pretest        # BooleanField - Has pretest?
    posttest       # BooleanField - Has posttest?
    languages      # ManyToMany(Language) - Supported languages
    point_total    # IntegerField - Grading points
    interactive    # BooleanField - Interactive training?
    logo_path      # CharField - Path to logo image
    feedback       # TextField - Grading feedback
```

### Language (`companies/models.py`)

```python
class Language:
    name           # CharField(100) - Language name
```

## Key Dependencies

- Django 4.1.7
- django-computed-property 0.3.0
- SQLite3 (default database)

## Development Commands

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Run development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

## Templates

All templates extend `static/templates/base.html`. Each app has its own templates in `<app>/templates/<app>/`.

## Admin Interface

Access at `/admin/` - manages Companies and Language models. Requires superuser account.

## Adding New Features

1. **New App**: `python manage.py startapp <name>`, add to `INSTALLED_APPS`
2. **New Model**: Define in `models.py`, run migrations, register in `admin.py`
3. **New View**: Create in `views.py`, add URL pattern in `urls.py`
4. **New Template**: Create in `<app>/templates/<app>/`, extend `base.html`
