# ASSETS Website - Association of Software Engineering Technology Students UGM

<p align="center">
 <img src="https://ugm.ac.id/images/logo-ugm.png" alt="UGM Logo" width="200"/>
</p>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/Laravel-11.x-red" alt="Laravel Version"></a>
  <a href="#"><img src="https://img.shields.io/badge/PHP-8.2%2B-blue" alt="PHP Version"></a>
  <a href="#"><img src="https://img.shields.io/badge/Status-Active-green" alt="Project Status"></a>
  <a href="#"><img src="https://img.shields.io/badge/License-MIT-yellow" alt="License"></a>
</p>

<div align="center">

  [🌐 Live Demo](https://assets.trpl.space/) • [📖 Official Repository](https://github.com/nadznaf/PAD1_Web-ASSETS) 
</div>

## 📋 Project Description

ASSETS Website is a semester-long simulated project aimed at building an inclusive and interactive website for the Association of Software Engineering Technology Students (ASSETS) UGM. This website is developed as an information platform and data management system for student organizations with comprehensive features for both admin and user.

Go to [📖 Official Repository](https://github.com/nadznaf/PAD1_Web-ASSETS)

**Development Period:** August 2024 - December 2024

## 👥 Development Team

| Name | Role | Contribution |
|------|------|------------|
| **Devangga Arya** | Project Manager | Project coordination, timeline management, stakeholder communication |
| **Zhazha** | UI/UX Designer | Interface design, user experience, prototyping |
| **Nadzira (Nafa)** | Frontend Developer | User interface implementation, responsive design |
| **Dwi** | Fullstack Developer | Backend and frontend development, system integration |

## 🚀 Main Features

### User Area
- **Student Profile**: Personal student data management
- **Cabinet Information**: Display ASSETS cabinet data per period
- **Staff & Divisions**: Organizational structure information
- **Work Programs**: List and details of organizational activities
- **Documentation**: Photo and video gallery of activities
- **Articles**: News portal and latest information

### Admin Area
- **Dashboard Analytics**: Statistics overview and organizational data
- **Student Management**: Member data CRUD operations
- **Lecturer Management**: Staff and supervisors
- **Cabinet Management**: Leadership data per period
- **Division Management**: Organizational structure
- **Staff Management**: Positions and roles
- **Work Program Management**: Activity planning and monitoring
- **Executor Management**: Task and responsibility assignment
- **Documentation Management**: Media upload and categorization
- **Time Management**: Activity scheduling
- **Color Palette Management**: Theme customization
- **Article Management**: Content publishing system

## 🛠️ Tech Stack

**Backend:**
- PHP 8.2+
- Laravel 11.x
- Eloquent ORM
- Artisan CLI

**Frontend:**
- Blade Templates
- HTML5 & CSS3
- JavaScript (ES6+)
- Tailwind CSS
- Bootstrap (components)

**Database:**
- MySQL/MariaDB

**Tools & Utilities:**
- Composer (dependency management)
- NPM/Yarn (package management)
- Vite (asset bundling)
- Git & GitHub (version control)

## 📊 Database Architecture

### Model Relationships
```
Kabinet (1) ←→ (n) Divisi ←→ (n) Staff ←→ (n) Mahasiswa
    ↓                              ↓
Dosen (1)                    Pelaksana (n)
    ↓                              ↓
ColorPalette (1)             Proker (n)
                                   ↓
                            WaktuProker (n)
                                   ↓
                            Dokumentasi (n)
```

### Main Entities
- **Mahasiswa**: Personal data of organization members
- **Dosen**: Supervisors and advisors data
- **Kabinet**: Leadership data per period
- **Divisi**: Internal organizational structure
- **Staff**: Positions and roles in organization
- **Proker**: Work programs and activities
- **Dokumentasi**: Media and activity archives
- **Artikel**: Content publishing system

## 🚀 Installation & Setup

### Prerequisites
- PHP >= 8.2
- Composer
- Node.js & NPM
- MySQL/MariaDB
- Git

### Installation Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/nadznaf/PAD1_Web-ASSETS.git
   cd PAD1_Web-ASSETS
   ```

2. **Install Dependencies**
   ```bash
   # Install PHP dependencies
   composer install
   
   # Install JavaScript dependencies
   npm install
   ```

3. **Environment Setup**
   ```bash
   # Copy environment file
   cp .env.example .env
   
   # Generate application key
   php artisan key:generate
   ```

4. **Database Configuration**
   ```bash
   # Edit .env file with database configuration
   DB_CONNECTION=mysql
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_DATABASE=assets_ugm
   DB_USERNAME=your_username
   DB_PASSWORD=your_password
   ```

5. **Database Migration & Seeding**
   ```bash
   # Run migrations
   php artisan migrate
   
   # Seed database (optional)
   php artisan db:seed
   ```

6. **Build Assets**
   ```bash
   # Development build
   npm run dev
   
   # Production build
   npm run build
   ```

7. **Start Development Server**
   ```bash
   php artisan serve
   ```

   Website will be available at `http://localhost:8000`

## 📁 Directory Structure

```
PAD1_Web-ASSETS/
├── app/
│   ├── Http/Controllers/     # Controller logic
│   ├── Models/              # Eloquent models
│   └── Providers/           # Service providers
├── database/
│   ├── migrations/          # Database migrations
│   ├── seeders/            # Database seeders
│   └── factories/          # Model factories
├── public/
│   ├── assets/             # Public assets
│   ├── css/                # Compiled CSS
│   ├── js/                 # Compiled JavaScript
│   └── imagesAdmin/        # Admin images
├── resources/
│   ├── views/              # Blade templates
│   ├── css/                # Source CSS
│   └── js/                 # Source JavaScript
├── routes/
│   ├── web.php             # Web routes
│   └── console.php         # Console commands
└── storage/                # File storage
```

## 🎯 Key Contributions

### Backend Development (Nadzira)
- **Database Design**: Comprehensive ERD (Entity Relationship Diagram) design
- **Migration System**: Created 12+ migration files for database structure
- **Documentation**: 
  - Data Flow Diagram (DFD)
  - Sequence Diagram
  - Backend API documentation
  - Route documentation
  - Variable documentation for frontend integration
- **User Section Backend**: Complete implementation using Laravel
- **Admin Section**: Development of 12 data management functionalities

### Implemented Management Features
1. Student Data Management
2. Lecturer Data Management  
3. Cabinet Data Management
4. Division Data Management
5. Staff Data Management
6. Work Program Management
7. Executor Management
8. Documentation Management
9. Work Program Time Management
10. Color Palette Management
11. Article Management
12. User Authentication Management

## 📖 Usage

### User Access
- Homepage: General organization information
- Profile: Personal student data
- Cabinet: Leadership information
- Activities: Work program list
- Documentation: Media gallery

### Admin Access
- Dashboard: Analytics and overview
- Data Management: CRUD operations for all entities
- Content Management: Article and content publishing
- User Management: Account and permission management

## 🔧 Development Workflow

1. **Work Breakdown Structure (WBS)**: Structured task planning and distribution
2. **Weekly Progress Updates**: Regular progress reports to stakeholders
3. **Collaborative Development**: Multi-role integration within one team
4. **Documentation-First Approach**: Complete technical documentation before implementation

## 🤝 Contributing

We welcome contributions from the community! To contribute:

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for complete details.

## 📞 Contact

**Project Maintainer:** Nadzira Nafa  
**GitHub:** [@nadznaf](https://github.com/nadznaf)  
**Institution:** Universitas Gadjah Mada

## 🙏 Acknowledgments

- **ASSETS UGM** - Association of Software Engineering Technology Students
- **Universitas Gadjah Mada** - Supporting institution
- **Laravel Community** - Framework and documentation
- **Tailwind CSS** - Styling framework
- **All Contributors** - Development team and stakeholders

---

<p align="center">
  Made with ❤️ by ASSETS Development Team | © 2024 ASSETS UGM
</p>
