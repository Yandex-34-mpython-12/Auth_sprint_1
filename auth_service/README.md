# Проектная работа 6 спринта

Ссылка на проект: https://github.com/Yandex-34-mpython-12/Auth_sprint_1


This repository contains the microservices for our application, including authentication (`auth_service`), film management (`film_service`), and an ETL (Extract, Transform, Load) process (`etl`). Each service requires specific environment configurations, which should be set up before running the services.

## Authentication Service
We use [FastAPI Users](https://fastapi-users.github.io/fastapi-users/latest/) to handle user management, including user creation and deletion. For authentication, we employ the Redis JWT strategy, which stores JWT tokens in a Redis cache to manage user sessions securely and efficiently.

## Setting Up Environment Variables

Each microservice in this project requires a `.env` file that contains necessary environment variables. These files should be created based on the `.env.example` files provided in each service's directory.

### Steps to Create `.env` Files

1. **Navigate to the Service Directory**:
   - `auth_service/`
   - `film_service/`
   - `etl/`

2. **Copy the `.env.example` File**:
   In each service directory, copy the `.env.example` file to create a new `.env` file. You can use the following command in your terminal:

   ```bash
   cp .env.example .env
   ```

3. **Edit the `.env` File**:
   Open the newly created `.env` file in a text editor and customize the environment variables according to your local development setup or production environment. For example:

   ```env
   # Example of environment variables in .env file
   APP_CONFIG__RUN__DEBUG=false
   APP_CONFIG__RUN__HOST=localhost
   APP_CONFIG__RUN__PORT=8000
   ```

4. **Create the `.es_state` File**:
Navigate to the  Directory:
   - `etl/`
and 

   ```bash
   cp es_state.json.example es_state.json
   ```

### Example Directory Structure

The structure of the repository should look like this:

```plaintext
project_root/
├── auth_service/
│   ├── .env.example
│   ├── .env        # <- Generated from .env.example
│   └── ...
├── film_service/
│   ├── .env.example
│   ├── .env        # <- Generated from .env.example
│   └── ...
├── etl/
│   ├── .env.example
│   ├── .env        # <- Generated from .env.example
│   └── ...
└── README.md
```

### Important Notes

- Ensure that all required environment variables are defined in the `.env` files to avoid runtime errors.
- If any variable is missing or incorrectly set, the services may fail to start or behave unexpectedly.
- Keep your `.env` files secure and never commit them to version control. Instead, share them securely with your team members as needed.

## Running the Services

After setting up the `.env` and `.es_state` files, you can start each service using the appropriate command, typically via Docker, `docker-compose up`.

## Accessing API Documentation
After setting up and running the services, you can find the API documentation at:

http://localhost:8001/api/openapi#/
This link provides access to the OpenAPI documentation for the API, allowing you to explore the available endpoints, request parameters, and responses.