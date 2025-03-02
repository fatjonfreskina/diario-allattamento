# breastfeeding-alexa

A FastAPI application that serves as the backend for an Alexa skill that helps breastfeeding mothers track their feeding sessions.

## Features

- **Add Feeding Session**: Allows users to add a new feeding session.
- **Get Feeding Sessions**: Allows users to get a list of all feeding sessions.

## Setup

### Prerequisites

- MySQL
- Python 3.8
- ngrok (for exposing your local server)

### Installation

1. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    . venv/bin/activate
    ```

2. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Create a [.env](http://_vscodecontentref_/1) file with your database credentials:

    ```plaintext
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_NAME=your_db_name
    DB_HOST_NAME=your_db_host
    DB_PORT=your_db_port
    ```

4. Run main script:

    ```sh
    fastapi dev src/main.py
    ```

### Exposing Your Local Server with ngrok

1. Download and install ngrok from [ngrok.com](https://ngrok.com/).

2. Start ngrok to expose your local server:

    ```sh
    ngrok http 8000
    ```

3. Copy the HTTPS URL provided by ngrok (e.g., `https://abcd1234.ngrok.io`).

4. In the Alexa Developer Console, set the endpoint for your skill to the ngrok URL followed by `/alexa/breastfeeding` (e.g., `https://abcd1234.ngrok.io/alexa/breastfeeding`).

### Running Migrations

1. Set up the environment variables:

    ```sh
    set DB_USER=your_db_user
    set DB_PASS=your_db_password
    set DB_NAME=your_db_name
    set HOST_NAME=your_db_host
    set HOST_PORT=your_db_port
    ```

2. Run the migrations:

    ```sh
    alembic upgrade head
    ```

### Testing

You can now test your Alexa skill using the Alexa Developer Console. Make sure your local server is running and exposed via ngrok.