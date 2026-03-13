## Prerequisites

- Python 3.9+
- PostgreSQL 12plus

## Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd flask-project 
```

### 2. Buat Virtual Environment 

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Window
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Database PostgreSQL

```bash
# Login ke PostgreSQL
psql -U postgres

# Buat database baru
CREATE DATABASE turbines;

# Keluar
\q
```

### 5. Konfigurasi Environment Variables

Copy file `.env.example` ke `.env`:

```bash
cp .env.example .env
```

Edit file `.env` dengan kredensial PostgreSQL Anda:

```env
PORT=5000
HOST=0.0.0.0
DEBUG=True
DB_HOST=localhost
DB_PORT=5432
DB_NAME=turbines
DB_USER=postgres
DB_PASSWORD=your_password
```

### 6. Jalankan Aplikasi

```bash
python3 app.py / python app.py
```

```bash
flask shell
```

### 7. Migration

```bash
flask db upgrade
```

or

```bash
flask db migrate -m ""
```
