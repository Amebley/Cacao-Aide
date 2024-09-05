# Cacao-Aide
A cocoa yield prediction and management system. Predicts cocoa yield, answers FAQs in cocoa farming, helps in farm records management and provides general information on cocoa farming.


## Features
1. **Yield Prediction**: Predict cocoa yield based on farmer input. Provide cocoa farming recommendation based on yield predictions.
2. **Record Management**: Keep track of farm diaries, inventory, and transactions.
3. **User Authentication**: Secure user login, registration and update of details.
4. **Chatbot**: Provides answers to frequently asked questions.
5. **Flash Messages**: Inform users about updates to their records and other actions.
6. **Tips and Info**: Provide cocoa farming tips based on yield predictions.

## Prerequisites
To run the application locally, you need to have the following installed:

- **Python 3.7+**
- **Flask**
- **SQLite (for database)**
- **Virtual Environment** (recommended)


## Setting Up the Application

### 1. Clone the Repository
First, clone the repository to your local machine:

```bash
git clone https://github.com/Amebley/Cacao-Aide.git
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

### 4. Set Up the Database
Initialize the SQLite database:

flask shell
>>> from models import db
>>> db.create_all()
>>> exit()

This will create the users.db file and initialize the tables for storing user information, diaries, inventories, and transactions.


5. Load the Cocoa Yield Model
Make sure you have the pre-trained cocoa_yield_model.pkl file in the project directory.

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
2. Update user input details.
3. Access cocoa farming tips.
4.  Use the yield prediction system by providing necessary inputs and receive recommendation based on inputs.
5. Add records for farm diaries, inventory, and transactions.
6. Manage records by viewing, editing, or deleting your stored data.
7. Access informing cocoa farming articles and detailed tutorial on cocoa cultivation.


Troubleshooting
Database Errors: Ensure that users.db exists and that you have correctly initialized the database tables using Flask's shell.

Model Loading Issues: If the cocoa yield model fails to load, ensure that the file cocoa_yield_model.pkl is in the root directory of the project.

Static Assets: Ensure the static files (CSS, images) are correctly placed in the static folder.


For any further assistance, feel free to raise an issue in the repository, or reach out to amebleyk@gmail.com.
