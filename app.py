import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, get_portfolio_metrics, login_required, usd

app = Flask(__name__)

app.jinja_env.filters["usd"] = usd

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ligação à base de dados project.db
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Garante que as respostas não fiquem em cache."""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Exibe as carteiras e análises guardadas do utilizador."""
    analyses = db.execute(
        "SELECT * FROM analyses WHERE user_id = ? ORDER BY created_at DESC",
        session["user_id"],
    )
    return render_template("index.html", analyses=analyses)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Inicia sessão do utilizador."""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return apology("Preencha o utilizador e a palavra-passe", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], password
        ):
            return apology("Utilizador ou palavra-passe inválidos", 400)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Regista um novo utilizador."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("Preencha todos os campos", 400)

        if password != confirmation:
            return apology("As palavras-passe não coincidem", 400)

        hash_pw = generate_password_hash(password)

        try:
            user_id = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username,
                hash_pw,
            )
            session["user_id"] = user_id
            return redirect("/")
        except ValueError:
            return apology("Nome de utilizador já existente", 400)

    return render_template("register.html")


@app.route("/logout")
def logout():
    """Termina a sessão."""
    session.clear()
    return redirect("/")


@app.route("/analyze", methods=["GET", "POST"])
@login_required
def analyze():
    """Executa a análise quantitativa de risco."""
    if request.method == "POST":
        tickers_raw = request.form.get("tickers")
        weights_raw = request.form.get("weights")
        portfolio_name = request.form.get("name", "Minha Carteira")

        if not tickers_raw or not weights_raw:
            return apology("Insira os ativos e os respetivos pesos", 400)

        tickers = [t.strip().upper() for t in tickers_raw.split(",")]

        try:
            weights = [float(w.strip()) for w in weights_raw.split(",")]
        except ValueError:
            return apology("Os pesos devem ser valores numéricos", 400)

        if len(tickers) != len(weights):
            return apology(
                "A quantidade de ativos e de pesos deve ser igual", 400
            )

        if abs(sum(weights) - 1.0) > 0.02:
            return apology(
                "A soma dos pesos deve ser igual a 1.0 (100%)", 400
            )

        try:
            metrics = get_portfolio_metrics(tickers, weights)

            # Guarda o resultado da análise na base de dados
            db.execute(
                "INSERT INTO analyses (user_id, portfolio_name, tickers, weights, exp_return, volatility, sharpe, var_95) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                session["user_id"],
                portfolio_name,
                tickers_raw.upper(),
                weights_raw,
                metrics["return"],
                metrics["volatility"],
                metrics["sharpe"],
                metrics["var_95"],
            )

            return render_template(
                "results.html",
                metrics=metrics,
                asset_weights=zip(tickers, weights),
                name=portfolio_name,
            )
        except Exception as e:
            return apology(f"Erro ao processar ativos: {str(e)}", 400)

    return render_template("analyze.html")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
