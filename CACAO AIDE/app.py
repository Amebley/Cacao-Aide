from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm, UpdateDetailsForm
from models import db, User, Diaries, Inventories, Transactions
import random
import joblib
import numpy as np
import json
import re
import nltk
from nltk.corpus import wordnet 
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging
from tips import COCOA_TIPS

app = Flask(__name__)

# Load your models
try:
    models = joblib.load('cocoa_yield_model.pkl')
    print("Models loaded successfully")
except Exception as e:
    print(f"Error loading models: {e}")
    models = None

# Define the mapping for 'location'
z = {'Dry': 0, 'Wet': 1, 'Mid': 2}

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'PAZZWORD'
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            flash('Username already exists. Please choose a different username.', 'danger')
        elif existing_email:
            flash('Email is already registered. Please choose a different email or log in.', 'danger')
        else:
            hashed_password = generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

# Home route leading to Content.html after login
@app.route('/home')
def home():
    return render_template('Content.html')

# Route for the 'Learn More' page
@app.route('/file')
def file():
    return render_template('file.html')

# Routes for the 6 content pages
@app.route('/Content1')
def content1():
    return render_template('Content1.html')

@app.route('/Content2')
def content2():
    return render_template('Content2.html')

@app.route('/Content3')
def content3():
    return render_template('Content3.html')

@app.route('/Content4')
def content4():
    return render_template('Content4.html')

@app.route('/Content5')
def content5():
    return render_template('Content5.html')

@app.route('/Content6')
def content6():
    return render_template('Content6.html')

@app.route('/dashboard')
@login_required
def dashboard():
    random_tip = random.choice(COCOA_TIPS)
    return render_template('dashboard.html', tip=random_tip, user=current_user)

@app.route('/update_details', methods=['GET', 'POST'])
@login_required
def update_details():
    form = UpdateDetailsForm()
    if form.validate_on_submit():
        if form.username.data:
            current_user.username = form.username.data
        if form.email.data:
            current_user.email = form.email.data
        if form.password.data:
            current_user.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Your account details have been updated!', 'success')
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        form.email.data = current_user.email
    return render_template('update_details.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



#Yield Prediction System
# Default values for fertilizers and insecticides if the user applies them
default_insecticide = 7.13
default_organic_fertilizer = 0.70
default_inorganic_fertilizer = 0.45

@app.route('/predict_yield', methods=['GET', 'POST'])
@login_required
def predict_yield():
    if request.method == 'POST':
        location = request.form['location']
        use_insecticides = request.form['insecticide.applied.ltrs.ha']
        use_organic_fertilizer = request.form['org.fert.kg.ha']
        use_inorganic_fertilizer = request.form['inorgfert.kg.ha']
        cocoa_plot_age = request.form['Cocoa plot age']
        cocoa_density = request.form['Cocoa plant density']

        # Map the 'location' value
        location_encoded = z.get(location)

        # Set values based on user input
        Insecticide = default_insecticide if use_insecticides.lower() == 'yes' else 0
        Organic_fertilizer = default_organic_fertilizer if use_organic_fertilizer.lower() == 'yes' else 0
        Inorganic_fertilizer = default_inorganic_fertilizer if use_inorganic_fertilizer.lower() == 'yes' else 0

        # Convert features to numpy array and reshape for prediction
        try:
            features = np.array([[location_encoded, Insecticide, Organic_fertilizer, Inorganic_fertilizer, int(cocoa_plot_age), int(cocoa_density)]], dtype=object).reshape(1, -1)
            print(f"Features: {features}")

            # Choose which model to use for prediction
            selected_model = models.get('model2')
            if selected_model and hasattr(selected_model, 'predict'):
                prediction = selected_model.predict(features)[0]
                prediction = round(prediction, 2)
                print(f"Prediction: {prediction}")

                # Flash message to scroll down
                flash("Scroll down for predicted yield and recommendations.")
                
                # Generate recommendations
                recommendations = []
                
                # Recommendation based on location
                if location == 'Dry':
                    recommendations.append("Consider planting in a mid or wet area for better results.")
                elif location == 'Mid':
                    recommendations.append("Area is okay, but moving to a more wet area might help increase yield.")
                elif location == 'Wet':
                    recommendations.append("You're in the best area for cocoa growth.")

                # Recommendation based on cocoa density
                if int(cocoa_density) < 600:
                    recommendations.append("Plant more trees or use a bigger plot to increase your yield.")
                elif 600 <= int(cocoa_density) <= 1500:
                    recommendations.append("The number of plants on the plot is good. You can maintain or increase it for increased yield.")
                else:
                    recommendations.append("Make sure your trees have enough space to grow well.")

                # Recommendation based on plot age
                if int(cocoa_plot_age) > 10:
                    recommendations.append("The plot may lack nutrients for increased yield because you have used it for long. Try leaving the plot for a while.")
                else:
                    recommendations.append("The plot may still be in good shape.")

                # Recommendations for insecticides and fertilizers
                if use_insecticides.lower() == 'no':
                    recommendations.append("Use insecticides in reduced quantities to prevent insects from destroying cocoa.")
                if use_organic_fertilizer.lower() == 'no':
                    recommendations.append("Think about adding organic fertilizers to your farming routine.")
                if use_inorganic_fertilizer.lower() == 'no':
                    recommendations.append("Consider using inorganic fertilizers for increased yield.")

                return render_template('predict_yield.html', prediction=prediction, recommendations=recommendations)
            else:
                print("Selected model is not correctly loaded or does not have a predict method")
                return "Model not loaded properly", 500
        except Exception as e:
            print(f"Error during prediction: {e}")
            return "Error during prediction", 500

    return render_template('predict_yield.html', user=current_user)


#Record Management system
@app.route('/farm_management', methods=['GET', 'POST'])
@login_required
def farm_management():
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        if form_type == 'diary':
            new_entry = Diaries(
                user_id=current_user.id,
                date=request.form['date'],
                activity=request.form['activity'],
                notes=request.form['notes']
            )
        elif form_type == 'inventory':
            new_entry = Inventories(
                user_id=current_user.id,
                item_name=request.form['item_name'],
                quantity_in_stock=request.form['quantity_in_stock'],
                last_updated=request.form['last_updated']
            )
        elif form_type == 'transaction':
            new_entry = Transactions(
                user_id=current_user.id,
                date=request.form['date'],
                description=request.form['description'],
                amount=request.form['amount'],
                transaction_type=request.form['transaction_type']
            )
        db.session.add(new_entry)
        db.session.commit()
        flash('Record added successfully! Scroll down to view all records', 'success')
        return redirect(url_for('farm_management'))

    diary_entries = Diaries.query.filter_by(user_id=current_user.id).all()
    inventory_items = Inventories.query.filter_by(user_id=current_user.id).all()
    transactions = Transactions.query.filter_by(user_id=current_user.id).all()
    return render_template('farm_management.html', diary_entries=diary_entries, inventory_items=inventory_items, transactions=transactions, user=current_user)

@app.route('/edit', methods=['POST'])
@login_required
def edit():
    form_type = request.form.get('form_type')
    id = request.form.get('id')
    if form_type == 'diary':
        entry = Diaries.query.get(id)
        entry.date = request.form['date']
        entry.activity = request.form['activity']
        entry.notes = request.form['notes']
    elif form_type == 'inventory':
        entry = Inventories.query.get(id)
        entry.item_name = request.form['item_name']
        entry.quantity_in_stock = request.form['quantity_in_stock']
        entry.last_updated = request.form['last_updated']
    elif form_type == 'transaction':
        entry = Transactions.query.get(id)
        entry.date = request.form['date']
        entry.description = request.form['description']
        entry.amount = request.form['amount']
        entry.transaction_type = request.form['transaction_type']
    db.session.commit()
    flash('Record updated successfully!', 'success')
    return redirect(url_for('farm_management'))

@app.route('/delete', methods=['POST'])
@login_required
def delete():
    form_type = request.form.get('form_type')
    id = request.form.get('id')
    if form_type == 'diary':
        entry = Diaries.query.get(id)
    elif form_type == 'inventory':
        entry = Inventories.query.get(id)
    elif form_type == 'transaction':
        entry = Transactions.query.get(id)
    db.session.delete(entry)
    db.session.commit()
    flash('Record deleted successfully!', 'success')
    return redirect(url_for('farm_management'))



#Chatbot
lemmatizer = WordNetLemmatizer()

# Synonym dictionary to handle variations in common phrases
synonym_dict = {
    "hey": "hello",
    "heya": "hello",
    "goodbye": "bye",
    "farewell": "bye",
    "sure": "alright",
    "right": "alright",
    "thanks": "thank you",
    "okay": "alright"
}

# Function to load FAQs from the file
def load_faqs():
    with open('static/faqs.json') as f:
        return json.load(f)

# Function to get the WordNet POS tag
def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

# Function to preprocess text
def preprocess(text):
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    tokens = nltk.word_tokenize(text.lower())
    lemmatized_tokens = [lemmatizer.lemmatize(token, get_wordnet_pos(token)) for token in tokens]
    return ' '.join(lemmatized_tokens)

# Function to replace synonyms in text
def synonym_replace(text):
    words = text.split()
    return ' '.join([synonym_dict.get(word, word) for word in words])

# Updated Preprocessing with Synonym Handling
def preprocess_with_synonyms(text):
    text = preprocess(text)
    return synonym_replace(text)

# Function to find the best matching FAQ using TF-IDF and cosine similarity
def find_answer(question, faqs):
    question = preprocess_with_synonyms(question)
    faq_questions = [preprocess_with_synonyms(faq['question']) for faq in faqs]
    
    # Combine the user question with the FAQ questions
    all_texts = [question] + faq_questions
    
    # Vectorize the texts using TF-IDF with n-grams
    vectorizer = TfidfVectorizer(ngram_range=(1, 3)).fit_transform(all_texts)
    vectors = vectorizer.toarray()
    
    # Compute cosine similarity between the user question and all FAQ questions
    cosine_similarities = cosine_similarity([vectors[0]], vectors[1:])
    
    # Find the index of the most similar FAQ question
    most_similar_index = cosine_similarities.argsort()[0][-1]
    similarity_score = cosine_similarities[0][most_similar_index]
    
    logging.debug(f"User Question: {question}")
    logging.debug(f"Matched FAQ Question: {faq_questions[most_similar_index]}")
    logging.debug(f"Similarity Score: {similarity_score}")
    
    # Set a threshold for similarity
    if similarity_score < 0.1:
        return "Sorry, I don't have an answer to that question."
    
    return faqs[most_similar_index]['answer']

@app.route('/chatbot', methods=['GET', 'POST'])
@login_required
def chatbot():
    response = ""
    question = ""
    if request.method == 'POST':
        question = request.form['question']
        faqs = load_faqs()
        response = find_answer(question, faqs)
    return render_template('chatbot.html', response=response, question=question, user=current_user)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
