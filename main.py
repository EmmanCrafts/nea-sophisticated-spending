"""
main.py - Flask application with all views/routes
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Transaction
from datetime import date, timedelta
from collections import defaultdict

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


VIDEOS = [
    {
        'title': 'Budgeting for Beginners',
        'url': 'https://www.youtube.com/results?search_query=budgeting+for+beginners',
        'keywords': 'budgeting saving money plan',
    },
    {
        'title': 'How to Save Money Every Month',
        'url': 'https://www.youtube.com/results?search_query=how+to+save+money+every+month',
        'keywords': 'saving money monthly tips',
    },
    {
        'title': 'What is Inflation?',
        'url': 'https://www.youtube.com/results?search_query=what+is+inflation+explained',
        'keywords': 'inflation economy prices',
    },
    {
        'title': 'Stock Market Explained for Beginners',
        'url': 'https://www.youtube.com/results?search_query=stock+market+explained+beginners',
        'keywords': 'stocks investing shares market',
    },
    {
        'title': 'How to Start Investing with Little Money',
        'url': 'https://www.youtube.com/results?search_query=how+to+start+investing+little+money',
        'keywords': 'investing stocks beginner small',
    },
    {
        'title': 'The 50/30/20 Budgeting Rule',
        'url': 'https://www.youtube.com/results?search_query=50+30+20+budgeting+rule',
        'keywords': 'budgeting rule saving spending',
    },
    {
        'title': 'What is Compound Interest?',
        'url': 'https://www.youtube.com/results?search_query=compound+interest+explained',
        'keywords': 'interest investing savings growth',
    },
    {
        'title': 'How to Be Frugal and Spend Less',
        'url': 'https://www.youtube.com/results?search_query=how+to+be+frugal+spend+less',
        'keywords': 'frugal spending saving tips',
    },
    {
        'title': 'Understanding Credit Cards and Debt',
        'url': 'https://www.youtube.com/results?search_query=understanding+credit+cards+debt',
        'keywords': 'credit cards debt borrowing',
    },
    {
        'title': 'Real Estate Investing for Beginners',
        'url': 'https://www.youtube.com/results?search_query=real+estate+investing+beginners',
        'keywords': 'real estate property investing housing',
    },
]


def search_videos(query):
    """
    Linear search through the video library.
    Returns videos where the query word appears in the title or keywords.
    """
    if not query:
        return VIDEOS  

    query = query.lower()
    results = []
    for video in VIDEOS:
        # Check title and keywords — simple linear scan
        if query in video['title'].lower() or query in video['keywords'].lower():
            results.append(video)
    return results


def get_dashboard_data(user_id):
    """
    Calculates all the stats needed for the Money Manager tab.
    Returns a dict so the dashboard route stays clean.
    """
    today = date.today()

    # All transactions for this user, newest first
    all_transactions = (Transaction.query
                        .filter_by(user_id=user_id)
                        .order_by(Transaction.date.desc())
                        .all())

    # --- Spending totals: only this calendar month ---
    monthly = [t for t in all_transactions
               if t.date.month == today.month and t.date.year == today.year]

    total_spent = sum(t.amount for t in monthly)

    # Category breakdown — simple loop, no libraries needed
    category_totals = defaultdict(float)
    for t in monthly:
        category_totals[t.category] += t.amount

    # --- Impulsive spending detection ---
    # Rule: same category appears 3 or more times in the last 7 days
    week_ago = today - timedelta(days=7)
    recent_week = [t for t in all_transactions if t.date >= week_ago]

    # Count how many times each category appears this week
    category_count = defaultdict(int)
    for t in recent_week:
        category_count[t.category] += 1

    # Collect the IDs of transactions that are "impulsive"
    impulsive_ids = {t.id for t in recent_week if category_count[t.category] >= 3}

    return {
        'transactions': all_transactions,
        'total_spent': total_spent,
        'category_totals': dict(category_totals),
        'impulsive_ids': impulsive_ids,
    }


# -------------------- ROUTES --------------------

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        session['user_id'] = user.id
        session['username'] = user.username

        if not user.survey_completed:
            return redirect(url_for('survey'))

        flash('Thanks for completing the survey — welcome back!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password', 'danger')
        return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        session['username'] = new_user.username
        return redirect(url_for('survey'))

    return render_template('register.html')


@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    user = User.query.get(session['user_id'])

    if user.survey_completed:
        flash('Thank you for completing the survey!', 'success')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        user.stakeholder_type = request.form.get('stakeholder_type')
        user.financial_goal = request.form.get('financial_goal')
        user.spending_frequency = request.form.get('spending_frequency')
        user.survey_completed = True
        db.session.commit()

        flash('Survey complete — welcome to Sophisticated Spending!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('survey.html', username=user.username)


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        flash('If an account exists with this email, you will receive reset instructions.', 'info')
        return redirect(url_for('index'))
    return render_template('forgot_password.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login to access the dashboard', 'warning')
        return redirect(url_for('index'))

    user = User.query.get(session['user_id'])
    data = get_dashboard_data(session['user_id'])

    # Education search — reads the 'q' query parameter from the URL
    video_query = request.args.get('q', '')
    videos = search_videos(video_query)

    return render_template('dashboard.html',
                           username=session.get('username'),
                           monthly_budget=user.monthly_budget,
                           video_query=video_query,
                           videos=videos,
                           **data)


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    description = request.form.get('description')
    amount = request.form.get('amount')
    category = request.form.get('category')
    date_str = request.form.get('date')

    if not description or not amount or not category or not date_str:
        flash('Please fill in all fields', 'danger')
        return redirect(url_for('dashboard'))

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
        transaction_date = date.fromisoformat(date_str)
    except ValueError:
        flash('Please enter a valid amount and date', 'danger')
        return redirect(url_for('dashboard'))

    transaction = Transaction(
        user_id=session['user_id'],
        description=description,
        amount=amount,
        category=category,
        date=transaction_date
    )
    db.session.add(transaction)
    db.session.commit()

    flash('Transaction added!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    """Delete a transaction — only if it belongs to the logged-in user"""
    if 'user_id' not in session:
        return redirect(url_for('index'))

    transaction = Transaction.query.get_or_404(transaction_id)

    # Safety check: make sure this transaction belongs to the current user
    if transaction.user_id != session['user_id']:
        flash('Not allowed', 'danger')
        return redirect(url_for('dashboard'))

    db.session.delete(transaction)
    db.session.commit()

    flash('Transaction deleted', 'info')
    return redirect(url_for('dashboard'))


@app.route('/set_budget', methods=['POST'])
def set_budget():
    """Save the user's monthly budget goal"""
    if 'user_id' not in session:
        return redirect(url_for('index'))

    budget = request.form.get('monthly_budget')

    try:
        budget = float(budget)
        if budget <= 0:
            raise ValueError
    except (ValueError, TypeError):
        flash('Please enter a valid budget amount', 'danger')
        return redirect(url_for('dashboard'))

    user = User.query.get(session['user_id'])
    user.monthly_budget = budget
    db.session.commit()

    flash('Budget goal updated!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))


# -------------------- RUN APP --------------------

if __name__ == '__main__':
    app.run(debug=True)
