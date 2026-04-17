```markdown
# All-PC Connection System

![Project Status](https://img.shields.io/badge/status-development-orange.svg)
![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Django Version](https://img.shields.io/badge/django-3.2+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 1. Overview

The All-PC Connection System is a robust, Django-based application designed for centralized management and monitoring of multiple client PCs, typically within a lab, classroom, or office environment. It facilitates seamless communication between a central server and individual client agents, providing administrators with a powerful dashboard to oversee and interact with connected machines.

This system aims to simplify the administration of a fleet of computers, enabling tasks such as status monitoring, remote command execution, and resource management from a single web interface.

## 2. Features

*   **Centralized Management Dashboard**: A web-based interface built with Django's admin capabilities for easy administration.
*   **Client Agent Communication**: `lab_agent.py` facilitates secure communication between client PCs and the `core_server`.
*   **PC Status Monitoring**: Track the online/offline status of connected client machines. (Implied)
*   **Database Integration**: Utilizes SQLite (default) for storing system data, client information, and administrative logs.
*   **Scalable Architecture**: Designed with a client-server model, allowing for easy expansion to manage more PCs.
*   **Secure Connection**: (Future/Implied) Mechanisms for secure agent-server communication.

## 3. Tech Stack

The project is built using the following core technologies:

*   **Python**: The primary programming language for both the server and client agents.
*   **Django**: The high-level Python web framework powering the `core_server` and its administrative dashboard.
*   **SQLite**: The default database for the Django project, suitable for development and small-scale deployments.
*   **pip**: Python package installer for managing dependencies.

## 4. Architecture

The system follows a classic client-server architecture:

*   **`core_server/`**: This is the heart of the system, a Django application responsible for:
    *   Serving the administrative dashboard (`admin_dashboard`).
    *   Providing an API for `lab_agent.py` to communicate with.
    *   Managing the database (`db.sqlite3`) for storing system and client data.
    *   Handling authentication and authorization for administrators.
*   **`lab_agent.py`**: This script runs on each client PC that needs to be managed. Its responsibilities include:
    *   Establishing a connection with the `core_server`.
    *   Sending status updates and system information to the server.
    *   Receiving and executing commands from the server.
*   **`db.sqlite3`**: The default database file for the Django server, storing all necessary application data.

```
LabManagerSystem/
├── core_server/                 # Django Server Application
│   ├── admin_dashboard/         # Admin interface components
│   ├── core_server/             # Django project settings & URL configs
│   ├── db.sqlite3               # SQLite Database
│   └── manage.py                # Django's administrative utility
└── lab_agent.py                 # Client-side agent script
```

## 5. Getting Started

Follow these instructions to set up and run the All-PC Connection System.

### Prerequisites

Ensure you have the following installed on your system:

*   **Python 3.8+**:
    ```bash
    python --version
    ```
*   **pip**: Python package installer (usually comes with Python).
    ```bash
    pip --version
    ```

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Akshay94os/All-Pc-connection-system.git
    cd All-Pc-connection-system/LabManagerSystem
    ```

2.  **Create and activate a virtual environment**:
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    Install all required Python packages using `pip` and the `require.txt` file.
    ```bash
    pip install -r ../require.txt
    ```
    *(Note: The `require.txt` file is expected in the parent directory based on the provided structure.)*

4.  **Apply database migrations**:
    Navigate into the `core_server` directory and apply initial database migrations to set up the SQLite database schema.
    ```bash
    cd core_server
    python manage.py migrate
    ```

5.  **Create a superuser (for admin dashboard access)**:
    This will allow you to log into the Django administration panel.
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create a username, email, and password.

### Configuration

The Django server's main configuration is located in `core_server/core_server/settings.py`.
For local development, no specific environment variables are strictly required beyond the default Django setup. However, for production, it's recommended to manage sensitive settings (like `SECRET_KEY`) via environment variables.

## 6. Usage

### Running the Django Development Server

From within the `core_server` directory (where `manage.py` is located):

```bash
python manage.py runserver
```

The server will typically start at `http://127.0.0.1:8000/`.

*   **Access the Admin Dashboard**: Open your web browser and navigate to `http://127.0.0.1:8000/admin/`. Log in with the superuser credentials you created earlier.

### Running the Client Agent

The `lab_agent.py` script is designed to run on client machines.

1.  **Ensure the server is running.**
2.  **Copy `lab_agent.py` to the client machine.**
3.  **Execute the agent script**:
    ```bash
    # On the client machine, navigate to where lab_agent.py is located
    python lab_agent.py
    ```
    *(Note: The `lab_agent.py` script will likely need configuration (e.g., server IP address/port) to connect to the `core_server`. This configuration might be hardcoded or passed as command-line arguments, which would need to be implemented within the script itself.)*

## 7. Development

### Setting up the Development Environment

1.  Follow the "Installation" steps above.
2.  Ensure your virtual environment is activated.
3.  The Django development server automatically reloads code changes, making development iterative.

### Running Tests

*(As no test files are provided, this section is a placeholder for future implementation.)*

To run tests for your Django application:

```bash
python manage.py test
```

### Code Style Guidelines

*   Follow PEP 8 for Python code style.
*   Use a linter like `flake8` or `pylint` to ensure code quality.

## 8. Deployment

For production deployments, consider the following:

1.  **Database**: Switch from SQLite to a more robust database like PostgreSQL or MySQL.
2.  **Web Server**: Use a production-ready web server like Gunicorn or uWSGI to serve the Django application.
3.  **Reverse Proxy**: Use Nginx or Apache as a reverse proxy to handle static files, SSL, and load balancing.
4.  **Environment Variables**: Manage sensitive settings (e.g., `SECRET_KEY`, database credentials) using environment variables.
5.  **Static Files**: Configure your web server to serve Django's static and media files efficiently.

## 9. API Documentation

The `core_server` implicitly provides an API for the `lab_agent.py` to communicate. Details of these endpoints would typically include:

*   **Agent Registration**: Endpoint for new agents to register with the server.
*   **Status Updates**: Endpoint for agents to send periodic health and status reports.
*   **Command Execution**: Endpoint for agents to receive and acknowledge commands from the server.

*(Detailed API documentation would be added here once specific endpoints are defined and implemented within the `core_server`.)*

## 10. Contributing

We welcome contributions to the All-PC Connection System! To contribute:

1.  **Fork the repository.**
2.  **Create a new branch** for your feature or bug fix: `git checkout -b feature/your-feature-name`.
3.  **Make your changes.**
4.  **Write clear, concise commit messages.**
5.  **Push your branch** to your forked repository.
6.  **Open a Pull Request** to the `main` branch of the original repository.

Please ensure your code adheres to the project's coding standards and includes relevant tests where applicable.

## 11. Troubleshooting

*   **`ImportError: Couldn't import Django...`**:
    *   Ensure Django is installed (`pip install django`).
    *   Verify your virtual environment is activated.
    *   Check `DJANGO_SETTINGS_MODULE` in `manage.py` is correctly set to `core_server.settings`.
*   **`OperationalError: no such table: ...`**:
    *   You likely forgot to run migrations: `python manage.py migrate`.
*   **Agent not connecting to server**:
    *   Check if the Django server is running (`python manage.py runserver`).
    *   Verify the server's IP address and port are correctly configured in `lab_agent.py`.
    *   Check firewall settings on both server and client machines.

## 12. Roadmap

*   Implement robust authentication for client agents.
*   Add remote command execution capabilities (e.g., shutdown, restart, software install).
*   Develop a comprehensive client monitoring dashboard with real-time data.
*   Integrate with a more advanced logging system.
*   Containerization using Docker for easier deployment.

## 13. License & Credits

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Developed by [Akshay94os](https://github.com/Akshay94os).
```