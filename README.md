# README for `sleepnumber` Application

This repository contains the necessary files for building, testing, and deploying the `sleepnumber` application which is an Alexa skill designed to control the SleepIQ bed settings. 

The application is deployed as an image to AWS ECR and executing using Lambda. 

## Prerequisites

- Docker installed
- AWS CLI installed and configured with necessary permissions
- Environment variables set in `.env` (see details below)

## Structure

- **makerfile**: Contains a list of commands to build, test, and deploy the application to AWS.
- **Dockerfile**: A Docker configuration file to build the Lambda function using AWS's Python 3.9 runtime.

## Configuration

### .env File

Before running any of the make commands, ensure you have the required environment variables in a `.env` file. The `makerfile` expects the following variables:

- AWS_ECR_ACCOUNT_ID: Your AWS account ID for the ECR repository
- AWS_ECR_REGION: AWS region for the ECR repository

The other parameters like APP_NAME and APP_VERSION are already set in the `makerfile`.

The application fetches secrets like `skill_id`, `username`, and `password` from AWS Secrets Manager.

## Functionality

The `sleepnumber` Alexa skill provides the following functionalities:

1. **Launch**: Initiates the skill and provides a welcome message.
2. **Set Firmness**: Sets the firmness of the bed to a specific value.
3. **Increase Firmness**: Increases the current firmness setting by 10, up to a maximum of 100.
4. **Session Ended**: Handles the termination of the Alexa skill session.

Additionally, the skill contains a catch-all exception handler to gracefully manage unexpected errors.

## Logging

All requests and responses are logged for debugging purposes.

## Implementation Details

- **main.py**:
    - Retrieves the skill secrets from AWS Secrets Manager.
    - Initializes the Alexa skill.
    - Registers request handlers, exception handlers, and interceptors.
    - Exports the Lambda handler.

- **services.py**:
    - Contains a `CustomAbstractRequestHandler` class that initializes the SleepIQ client using the provided secrets.
    - Contains various request handlers for the intents.
    - Contains request and response logging interceptors.

## Commands

### Build the Docker Image

```
make docker/build
```

This will create a Docker image for the application.

### Push the Docker Image to ECR

```
make docker/push TAG=dev
```

This command will:

1. Log in to AWS ECR
2. Tag the Docker image with the specified version/env
3. Push the Docker image to ECR
4. Update the Lambda function code with the new image

### Run the Docker Image Locally

```
make docker/run
```

This runs the Docker image locally, exposing it on port 9000.

### Test the Local Docker Image

```
make docker/test
```

This sends a test POST request to the locally running Docker image.

## Dockerfile Details

The Dockerfile is based on the AWS Lambda Python 3.9 runtime. It will:

1. Install any dependencies specified in `requirements.txt`
2. Copy the source code from `src` to the Lambda task root
3. Set `main.handler` as the command to be executed when the Lambda function is triggered
