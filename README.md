# Multi-Source Data Shipper

This project is a modular data shipper that collects data from multiple sources (e.g., OpenWeatherMap, WeatherAPI.com), normalizes it, and ships it to a Logz.io account using Fluent Bit.

---

## Table of Contents

- [Features](#features)
- [Prerequisites & Setup](#prerequisites--setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Running Unit Tests](#running-unit-tests)
- [Docker](#docker)
- [CI/CD](#cicd)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- Fetches data from multiple sources
- Configurable polling interval
- Ships logs to Logz.io using the HTTP Bulk endpoint
- Supports unit testing with Python `unittest` and `mock`
- Modular architecture for easy extension

---

## Prerequisites & Setup

### Logz.io Account

1. Create a free trial account here: [Logz.io Free Trial](https://logz.io/free-trial).  
   You can use an organization email or a temporary email service, for example: [Temp-Mail](https://temp-mail.org/en/).  

2. After signing up, navigate to **Logs > Send Your Data > HTTP** and note:  
   - **Shipping Token**  
   - **Listener Host**

### Development Environment

- Ensure you have your preferred programming language installed (Python, Go, Node.js, Java, etc.).  
- Ensure you have **Git** and **Docker** installed.  

### API Keys

- **OpenWeatherMap**: Sign up for a free account and get an API key at [OpenWeatherMap](https://openweathermap.org/).  
- **WeatherAPI.com**: Sign up for a free account and get an API key at [WeatherAPI.com](https://www.weatherapi.com/).  

---

## Configuration

The application uses a `config.template.yaml` file for configuration. Example:

```yaml
polling_interval: 60
logzio:
  listener_host: "listener-ca.logz.io"
  shipping_token: "YOUR_LOGZIO_TOKEN"
sources:
  - type: openweathermap
    api_key: "YOUR_OPENWEATHERMAP_API_KEY"
    location: "London,GB"
  - type: weatherapi
    api_key: "YOUR_WEATHERAPI_KEY"
    location: "London"
Notes:

Replace YOUR_LOGZIO_TOKEN with your Logz.io shipping token.

Replace API keys with your own from the respective services.

polling_interval is in seconds.

Running the Application
Activate your virtual environment (if using Python):

Run the data shipper:

bash
Copy code
python DataShipper.py 
The application will fetch data from the configured sources and ship logs to Logz.io at the specified interval.

Running Unit Tests
bash
Copy code
python -m unittest test.py
External API calls are mocked using unittest.mock.

Ensure your virtual environment is active.

Docker
Build the Docker image:

bash
Copy code
docker build -t my-app .
Run the container:

bash
Copy code
docker run my-app

Ensure Docker Desktop is running.

CI/CD
GitHub Actions pipeline available at .github/workflows/ci.yml.

Add DOCKER_USERNAME and DOCKER_PASSWORD to GitHub Secrets.

Contributing
Fork the repository

Create a feature branch

Commit changes with clear messages

Open a pull request

License
This project is licensed under the MIT License.
