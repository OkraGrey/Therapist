# The Therapist - Django Application

A comprehensive Django-based application for managing therapeutic forms and patient responses.

## 🚀 Project Overview

The Therapist is a modular Django application designed to handle form creation, management, and patient submissions. The project follows a scalable architecture with clear separation of concerns and is built to grow into a larger healthcare management system.

## 📋 Features

### Phase 1: Core Setup & User Authentication ✅
- [x] Django project setup with optimal configuration
- [x] MySQL database integration
- [x] Custom user model with extended fields
- [x] Complete authentication flow (registration, login, logout)
- [x] Email verification system
- [x] Password management
- [x] Admin role enforcement

### Phase 2: Form Management (Admin) 🔄
- [ ] Admin dashboard
- [ ] Form creation and management
- [ ] Question types (text, multi-choice, range)
- [ ] Dynamic form builder interface

### Phase 3: Public Form Usage & Submission 📝
- [ ] Public form access
- [ ] Form submission handling
- [ ] Response storage
- [ ] Email confirmations

### Phase 4: Refinement & Future Considerations 🎨
- [ ] UI/UX enhancements
- [ ] Error handling
- [ ] Advanced admin features
- [ ] Analytics and reporting

## 🛠️ Technology Stack

- **Backend**: Django 4.2+
- **Database**: MySQL 8.0+
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Email**: Django's email backend
- **Authentication**: Django's built-in auth system with custom user model

## 📁 Project Structure

```
therapist_project/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── docs/
│   └── CONTEXT.md
├── therapist_project/          # Main project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                   # User authentication app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── migrations/
│   └── templates/accounts/
├── forms/                      # Form management app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── migrations/
│   └── templates/forms/
├── submissions/                # Form submissions app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── migrations/
│   └── templates/submissions/
├── core/                       # Core utilities and base templates
│   ├── __init__.py
│   ├── middleware.py
│   ├── utils.py
│   └── templates/core/
├── static/                     # Static files
│   ├── css/
│   ├── js/
│   └── images/
└── media/                      # User uploaded files
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd therapist_project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database and email settings
   ```

5. **Database setup**
   ```bash
   # Create MySQL database
   mysql -u root -p
   CREATE DATABASE therapist_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   
   # Run migrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

## 🔧 Configuration

### Environment Variables (.env)

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=therapist_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Static and Media
STATIC_URL=/static/
MEDIA_URL=/media/
```

## 🏗️ Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings for all functions and classes
- Keep functions small and focused

### Git Workflow
- Create feature branches for new features
- Use descriptive commit messages
- Test thoroughly before merging
- Update documentation for new features

### Testing
- Write unit tests for models and views
- Use Django's test framework
- Maintain good test coverage

### Security Best Practices
- Never commit sensitive data (API keys, passwords)
- Use environment variables for configuration
- Validate all user inputs
- Implement proper authentication and authorization

## 📊 Database Schema

### Core Models

#### Custom User Model
- `email` (unique identifier)
- `first_name`, `last_name`
- `gender`, `age`, `country`
- `is_verified`, `date_verified`
- `created_at`, `updated_at`

#### Form Management
- `Form`: name, description, created_by, created_at
- `Question`: form (FK), text, type, is_mandatory, order
- `ChoiceOption`: question (FK), text, order

#### Submissions
- `Submission`: form (FK), submitted_at, email
- `Answer`: submission (FK), question (FK), text_answer, choice_answer (FK), range_answer

## 🔄 API Endpoints

### Authentication
- `POST /accounts/register/` - User registration
- `POST /accounts/login/` - User login
- `POST /accounts/logout/` - User logout
- `GET /accounts/verify/<token>/` - Email verification

### Forms (Admin)
- `GET /admin/dashboard/` - Admin dashboard
- `GET /admin/forms/create/` - Create form page
- `POST /admin/forms/create/` - Save new form
- `GET /admin/forms/<id>/` - View form details

### Public Forms
- `GET /forms/<id>/` - Public form view
- `POST /forms/<id>/submit/` - Submit form responses

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure production database
- [ ] Set up static file serving
- [ ] Configure email backend
- [ ] Set up SSL/HTTPS
- [ ] Configure logging
- [ ] Set up monitoring

### Docker Deployment
```bash
# Build and run with Docker
docker-compose up --build
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation in `/docs/`

## 📈 Roadmap

- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Mobile app integration
- [ ] API for third-party integrations
- [ ] Advanced reporting features
- [ ] Patient management system
- [ ] Appointment scheduling
- [ ] Payment integration

---

**Built with ❤️ using Django** 