from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# App configuration
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Database setup
db = SQLAlchemy(app)

# Expense model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(20), nullable=False)

# Create database
with app.app_context():
    db.create_all()

# Routes
@app.route("/")
def index():
    expenses = Expense.query.all()
    total_expense = sum(expense.amount for expense in expenses)  # Calculate total expense
    return render_template("index.html", expenses=expenses, total_expense=total_expense)

@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        title = request.form["title"]
        amount = request.form["amount"]
        category = request.form["category"]
        date = request.form["date"]

        new_expense = Expense(title=title, amount=float(amount), category=category, date=date)
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add_expense.html")

@app.route("/delete/<int:id>")
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for("index"))

# Run app
if __name__ == "__main__":
    app.run(debug=True)
