fastesc
================

fastesc is an API for various Eurovision Song Contest related data.

## Requirements

- **Python Version**: 3.13+
- **Dependencies**:  Found in `requirements.txt`
- **Database**: postgreSQL Server

## Getting Started

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/your-project-name.git
   ```
2. **Set .env variables**
    * Use the .env variable at the root level
    * or use one at ````etc/secrets/.env````
3. **Run the migration script**
   ```bash
   python -m fastesc.scripts.migrate
   ```
4. **Run the Api**
    * using fastapi
   ```bash
   fastapi run fastesc/main.py
   ```
    * or Docker
   ```bash
   docker build  -t fastesc .
   docker run fastesc
   ```

### Testing

If you want to run the tests you have to create a database with name "test" in your database system.

```bash
pytest 
```
