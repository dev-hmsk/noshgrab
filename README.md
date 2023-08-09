# NoshGrabService

NoshGrab is a web application designed to provide a seamless experience for food ordering and management. Built with Flask and backed by a PostgreSQL database, it offers robust features and integrations to ensure a smooth user experience.

# Prerequisites
- Python 3.x
- Docker
- PostgreSQL
- AWS Credentials (for AWS EC2 Hosting)
- Vault (for secret management)

# Installation & Setup
Clone the Repository:

git clone https://github.com/dev-hmsk/noshgrab.git
cd noshgrab

# Setup Virtual Environment:
Navigate to the scripts/setup directory and run the virtual environment setup script.

# Install Dependencies:

pip install -r requirements.txt

# Database Setup:
Use the provided Dockerfile for PostgreSQL to set up the database container.

# AWS & Vault Configuration:
Navigate to the scripts/setup directory and follow the instructions for AWS and Vault setup.

# Run the Application:
python app.py

# Systemd Services
For those looking to run noshgrab as a service, systemd service files are provided for both the main application and Vault. These can be found in the systemd_service directory.

# Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

# License
Please refer to the repository's license file for information on licensing.

