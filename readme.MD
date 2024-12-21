# Design Gen

Welcome to the Design Gen project! Follow these steps to set up your development environment and get the server running.

## Setup

### Step 1: Install Pylint

Ensure you have the Pylint extension installed in Visual Studio Code for code linting. You can get it [here](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint).

### Step 2: Create a Virtual Environment

Set up a virtual environment to manage your project dependencies:

```sh
python3 -m venv env
```

### Step 3: Install Dependencies

Navigate to the backend directory and install the required dependencies:

```sh
cd backend
pip install -r requirements.txt
```

## Running the Server

Run the following command to set anthropic api key:

```sh
export ANTHROPIC_API_KEY=your_api_key
```

Start the development server with the following command:

```sh
python manage.py runserver
```

You're all set! Happy coding!
