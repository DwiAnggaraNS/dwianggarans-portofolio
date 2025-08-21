# 🎓 LSP UGM - Professional Certification Platform

<div align="center">
  <img src="https://ugm.ac.id/images/logo-ugm.png" alt="UGM Logo" width="200"/>
  
  [![Laravel](https://img.shields.io/badge/Laravel-v10.x-FF2D20?style=for-the-badge&logo=laravel&logoColor=white)](https://laravel.com)
  [![PHP](https://img.shields.io/badge/PHP-8.2+-777BB4?style=for-the-badge&logo=php&logoColor=white)](https://php.net)
  [![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://mysql.com)
  [![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

  **An official certification platform for Universitas Gadjah Mada (UGM)**
  
  *Facilitating professional certification processes for students, lecturers, and educational staff in compliance with BNSP national standards*

  [🌐 Live Demo](https://silsp.trpl.space/) • [📖 Official Repository](https://github.com/annisa-ugm/PAD-LSP-UGM) 
</div>

---

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Team](#team)
- [Contributing](#contributing)
- [License](#license)

## 🎯 About

LSP UGM is a comprehensive web-based professional certification platform designed specifically for Universitas Gadjah Mada. The system streamlines the certification process for various stakeholders while maintaining compliance with **Badan Nasional Sertifikasi Profesi (BNSP)** standards.

Go to [📖 Official Repository](https://github.com/annisa-ugm/PAD-LSP-UGM) 

### 🚀 Project Background

This project follows a **phased development approach**:

**Phase 1**: Initial development by previous team (legacy codebase with technical debt and business logic issues)

**Phase 2** (Feb 2025 - Jun 2025): **Our Team's Contributions**
Our team (PAD 2 Arya) was tasked with comprehensive system refactoring and new feature development:

#### 🔧 Refactoring PAD1 (7 Major Improvements):
1. **Authentication System**: Refactored account creation with Google OAuth integration (Full-stack)
2. **Schema Management**: Complete overhaul of Skema (CRU), UK (CRU), and Elemen UK (CRU) modules (Full-stack + ERD)
3. **Assignment System**: Refactored Asesi-to-Asesor assignment workflow (Full-stack + ERD)
4. **Assessment Planning**: Complete "Rencana Asesmen" module reconstruction (Full-stack CRUD + ERD)
5. **Digital Signatures**: Implemented isolated signature storage system to prevent form corruption during updates (Full-stack + ERD)
6. **APL1 Module**: Complete frontend and backend restructuring
7. **Primary Key Generation**: Fixed potential errors across **32 files** with improved UUID generation system

#### ⚡ New Features PAD2 (8 Core Modules):
8. **Biodata Form** (Asesor role)
9. **Kompetensi Teknis Asesor** (Admin & Asesor roles)
10. **FR.APL.02** (Asesor & Asesi roles)
11. **FR.AK.01** (Asesor & Asesi roles)
12. **Konsul Pra Uji** (Asesor & Asesi roles)
13. **FR.MAPA.01** - Assessment Activity Planning (Asesor role)
14. **FR.MAPA.02** - Assessment Instrument Mapping (Asesor role)
15. **Pernyataan Ketidakberpihakan** - Impartiality Declaration (Asesor & Asesi roles)

**Phase 3** (Current): Continued development by a different team

> **📌 Disclaimer**: This repository represents the work completed during **Phase 2** of the project. The platform is currently being enhanced in **Phase 3** by a different development team.

### 👥 User Roles

| Role | Description |
|------|-------------|
| **Visitor** | Browse public information and certification details |
| **Asesi** | Students/staff applying for professional certification |
| **Asesor** | Certified assessors evaluating competency |
| **Admin** | System administrators managing the platform |

## ✨ Features (Phase 2 Contributions)

### 🔐 Authentication & Authorization
- **Google OAuth Integration**: Streamlined account creation process
- Multi-role authentication system
- API key-based security
- Role-based access control (RBAC)

### 📊 Assessment Management (Complete Module Suite)
- **Konsultasi Pra-Uji**: Pre-assessment consultation workflow
- **FR.MAPA.01**: Assessment activity and process planning
- **FR.MAPA.02**: Assessment instrument mapping and planning
- **FR.AK.01**: Assessment agreement & confidentiality forms
- **FR.APL.02**: Competency portfolio management
- **Ketidakberpihakan**: Impartiality declaration system

### 🎛️ Admin Dashboard (Fully Refactored)
- **Schema Management**: Complete CRUD for Skema, UK, and Elemen UK
- **Assignment System**: Enhanced Asesi-to-Asesor workflow
- **Assessment Planning**: Comprehensive "Rencana Asesmen" module
- **Digital Signature Management**: Isolated storage system
- **Primary Key Generation**: Robust UUID system across 32 files

### 👤 User Management
- **Biodata Management**: Comprehensive Asesor profile system
- **Kompetensi Teknis**: Technical competency tracking for Asesors
- **Role-based Dashboards**: Customized interfaces for each user type

### 🔒 Data Integrity & Security
- **Signature Isolation**: Prevents form corruption during updates
- **API Documentation**: Complete Swagger/OpenAPI 3.0 integration
- **Error Handling**: Comprehensive validation and error management

## 🛠️ Tech Stack

**Backend:**
- PHP 8.2+
- Laravel 10.x
- Laravel Sanctum
- MySQL 8.0+

**Frontend:**
- Blade Templates
- HTML5 & CSS3
- JavaScript (ES6+)
- Bootstrap 5

**API & Documentation:**
- RESTful API
- Swagger/OpenAPI 3.0

**Development Tools:**
- Composer
- Git & GitHub
- Kanban (Project Management)

## 🚀 Getting Started

### Prerequisites

- PHP >= 8.2
- Composer
- MySQL >= 8.0
- Node.js & NPM (for frontend assets)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/annisa-ugm/PAD-LSP-UGM.git
   cd PAD-LSP-UGM
   ```

2. **Install PHP dependencies**
   ```bash
   composer install
   ```

3. **Install NPM dependencies**
   ```bash
   npm install
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   php artisan key:generate
   ```

5. **Database configuration**
   ```bash
   # Update your .env file with database credentials
   DB_CONNECTION=mysql
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_DATABASE=lsp_ugm
   DB_USERNAME=your_username
   DB_PASSWORD=your_password
   ```

6. **Run migrations and seeders**
   ```bash
   php artisan migrate --seed
   ```

7. **Generate API documentation**
   ```bash
   php artisan l5-swagger:generate
   ```

8. **Start the development server**
   ```bash
   php artisan serve
   ```

9. **Compile frontend assets**
   ```bash
   npm run dev
   ```

### 🔑 API Key Setup

For API access, you'll need to configure API keys:

```bash
php artisan tinker
```

```php
// Generate API key for development
$apiKey = \Str::random(32);
echo $apiKey;
```

Add the generated key to your `.env`:
```
API_KEY=your_generated_api_key
```

## 📖 API Documentation

Our API is fully documented using Swagger/OpenAPI 3.0. Access the interactive documentation at:

**Local:** `http://localhost:8000/api/documentation`

### Key API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/asesor/biodata/{id}` | GET | Get assessor profile |
| `/api/v1/asesmen/ak01/{id_asesi}` | GET | Get AK01 form data |
| `/api/v1/asesmen/mapa01/{id_asesi}` | GET | Get MAPA01 assessment |
| `/api/v1/asesmen/konsultasi-prauji/{id_asesi}` | GET | Get pre-assessment consultation |

### Authentication

All API requests require an API key in the header:
```bash
curl -H "X-API-KEY: your_api_key" https://lsp.ugm.ac.id/api/v1/endpoint
```

## 📁 Project Structure

```
PAD-LSP-UGM/
├── app/
│   ├── Http/
│   │   └── Controllers/
│   │       └── Api/                    # API Controllers
│   │           ├── Asesmen/            # Assessment modules
│   │           └── DataUser/           # User data management
│   ├── Models/                         # Eloquent models
│   ├── Services/                       # Business logic services
│   └── Helpers/                        # Helper classes
├── resources/
│   ├── views/                          # Blade templates
│   ├── css/                           # Stylesheets
│   └── js/                            # JavaScript files
├── routes/
│   ├── web.php                        # Web routes
│   └── api.php                        # API routes
├── database/
│   ├── migrations/                     # Database migrations
│   └── seeders/                       # Database seeders
└── storage/
    └── api-docs/                      # Generated API documentation
```

## 👨‍💻 Team PAD 2 (Phase 2 Development)

| Role | Name | Contributions |
|------|------|---------------|
| **Project Manager** | Devangga Arya | Project coordination, stakeholder management, Kanban workflow |
| **UI/UX Designer** | Zhazha | Interface design, user experience optimization |
| **Frontend Developer** | Nadzira (Nafa) | Frontend implementation, responsive design |
| **Fullstack Developer** | Dwi | Full-stack development, system integration |
| **Backend Developer** | Annisa | API development, database optimization, system architecture |

> **Note**: This project is currently in **Phase 3** development with a different team continuing the enhancement work. 

## 🤝 Contributing

We welcome contributions from the community! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Workflow

- We use **Kanban methodology** for project management
- Follow **SOLID principles** in code development
- Ensure API endpoints are properly documented
- Write meaningful commit messages
- Test thoroughly before submitting PRs

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Universitas Gadjah Mada** for the project opportunity
- **BNSP** for certification standards guidance
- Laravel community for excellent framework and documentation
- All contributors who helped improve this platform

## ⚠️ Important Notice

This repository represents the **Phase 2 development** of the LSP UGM platform (February 2025 - June 2025). The project has entered **Phase 3** and is currently being developed by a different team. 

**For current development status and latest features, please contact the current development team or UGM LSP administrators.**

---

<div align="center">
  <p>Made with ❤️ by Team PAD 2 - UGM Development</p>
  <p>© 2025 Universitas Gadjah Mada. All rights reserved.</p>
  <p><strong>Phase 2 Development: February 2025 - June 2025</strong></p>
</div>
