# Cacao-Aide
A cocoa yield prediction and management system. Predicts cocoa yield, answers FAQs in cocoa farming, helps in farm records management and provides general information on cocoa farming.


## Features
1. **Yield Prediction**: Predict cocoa yield based on farmer input. Provide cocoa farming recommendation based on yield predictions
2. **Record Management**: Keep track of farm diaries, inventory, and transactions.
3. **User Authentication**: Secure user login and registration.
4. **Chatbot**: Provides answers to frequently asked questions and helps users navigate the app.
5. **Flash Messages**: Inform users about updates to their records and other actions.
6. **Tips and Info**: Provide cocoa farming tips based on yield predictions.

## Prerequisites
To run the application locally, you need to have the following installed:

- **Python 3.7+**
- **Virtual Environment** (Optional but recommended)

## Setting Up the Application

### 1. Clone the Repository
First, clone the repository to your local machine:

```bash
git clone <repository-url>
cd CACAO AIDE
```

### 2. Set Up a Virtual Environment
(Optional but recommended to avoid dependency conflicts)

```bash
# Install virtualenv if you don't have it
pip install virtualenv

# Create a virtual environment
virtualenv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
Install the required Python packages listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory of the project to store environment variables:

```bash
touch .env
```

Add the following variables to your `.env` file:

```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

Ensure to replace `your_secret_key_here` with a strong secret key.

### 5. Set Up the Database
Before running the app, you need to initialize the SQLite database:

```bash
# Open the Python shell to set up the database
python
```

In the Python shell, run:

```python
from app import db
db.create_all()
exit()
```

### 6. Run the Application
Now you are ready to run the application:

```bash
flask run
```

You should see output indicating that the Flask server is running, such as:

```bash
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Visit `http://127.0.0.1:5000/` in your browser to use the application.

## Usage
Once the application is running, you can:

1. Register a new account or log in with an existing account.
2. Add records for farm diaries, inventory, and transactions.
3. Use the yield prediction system by providing necessary inputs.
4. Manage records by viewing, editing, or deleting your stored data.

## Testing
To test that everything works, use the following commands:

```bash
# Running tests
pytest
```

## Troubleshooting
If you encounter any issues, ensure that:

1. **Dependencies**: All dependencies are properly installed using the `requirements.txt` file.
2. **Database Setup**: The SQLite database has been properly initialized.
3. **Environment Variables**: The `.env` file is correctly set up.

For any further assistance, feel free to raise an issue in the repository.
