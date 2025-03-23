# Diario allattamento

![GitHub Workflow Status](https://github.com/fatjonfreskina/diario-allattamento/actions/workflows/docker_push.yaml/badge.svg)

---

<table>
  <tr>
    <td>
      <p>
        A FastAPI application that serves as the backend for an Alexa skill that helps breastfeeding mothers track their feeding sessions.
      </p>
    </td>
    <td>
      <img src="media/logo.jpg" alt="drawing" width="200" style="border-radius: 50%; border: 2px solid #000; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);"/>
    </td>
  </tr>
</table>

## Table of Contents

- [Diario allattamento](#diario-allattamento)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Exposing Your Local Server with ngrok](#exposing-your-local-server-with-ngrok)
    - [Running Migrations](#running-migrations)
    - [Testing](#testing)
  - [Contributing](#contributing)

## Features

- **Add Feeding Session**: Allows users to add a new feeding session.
- **Get Feeding Sessions**: Allows users to get a list of all feeding sessions.

## Setup

### Prerequisites

- MySQL
- Python 3.8
- ngrok (for exposing your local server)
- Alexa Developer Console account

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

3. Create a `.env` file with your database credentials:

    ```plaintext
    DB_USER=your_db_user
    DB_PASS=your_db_password
    HOST_NAME=your_db_host
    HOST_PORT=your_db_port
    DB_NAME=your_db_name
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

4. In the Alexa Developer Console, set the endpoint for your skill to the ngrok URL (e.g., `https://abcd.ngrok-free.app`).

### Running Migrations

1. Set up the environment variables:

    ```sh
    set DB_USER=your_db_user
    set DB_PASS=your_db_password
    set HOST_NAME=your_db_host
    set HOST_PORT=your_db_port
    set DB_NAME=your_db_name
    ```

2. Run the migrations:

    ```sh
    alembic upgrade head
    ```

### Testing

You can now test your Alexa skill using the Alexa Developer Console. Make sure your local server is running and exposed via ngrok.

On the Alexa Developer Console, you can test your skill by invoking it with the following utterances:

- "Alexa, apri Diario allattamento"
- "Alexa, aggiungi allattamento a destra"
- "Alexa, quando è stato l'ultimo allattamento?"

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
