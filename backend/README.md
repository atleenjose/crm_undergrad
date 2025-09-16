# Backend

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/atleenjose/crm_undergrad.git
   cd crm_undergrad/backend

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # Mac/Linux

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Set up environment variables:
    Add your Firebase service key JSON file (not included in the repo for security)

5. .gitignore and Sensitive Files
    This repository uses a .gitignore file to prevent pushing sensitive files, such as the Firebase service key and the Python virtual environment (venv/).
    Make sure to add your own service key locally before running the project.

6. Run the project:
    ```bash
    python app.py

7. Notes
    Python 3.9+ recommended
    Deactivate the virtual environment when done:
        ```bash
        deactivate
    