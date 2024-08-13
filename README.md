# Project name

Python-Assignments

## Description

Project consists of three main parts:
1. Code reviews
2. Python tasks 
3. A simple recommendation system consisting of the following services: 1. Generaor 2. Invoker

## Folder Structure

- **code_reviews/**: Contains various Python code snippets that need to be reviewed.
- **tasks/**: Includes separate Python file for each task.
- **services/**: Contains directories for different services:
  - **generator/**: Contains code and configuration for the generator service.
  - **invoker/**: Contains code and configuration for the invoker service.

## Setup Instructions

1. **Clone the Repository**:

git clone <repository-url>

2. **Build Docker For Services**

Build docker for both generator and invoker services:
    docker build -t generator_service . 
    docker build -t invoker_service .
Build docker for redis:
    docker pull redis:latest
Run docker containers for services
    docker run -d -p 5000:5000 --name generator_service generator_service  
    docker run -d -p 5001:5001 --name invoker_service invoker_service
Run docker container for redis
    docker run -d --name redis -p 6379:6379 redis:latest
To send correct POST requests to services, use curl:
    Invoker service
    curl --header "Content-Type: application/json" --request POST --data '{"user_id": 132}' http://localhost:5001/recommend
    Generator service
    curl --header "Content-Type: application/json" --request POST --data '{"model_name": "Blaster", "viewerid": 132}' http://localhost:5000/generate_recommendation


