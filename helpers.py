from functools import wraps
import numpy as np
import pandas as pd
from flask import redirect, render_template, session
import yfinance as yf


def apology(message, code=400):
    """Renderiza uma mensagem de erro estilizada."""

    def escape(s):
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """Exige login para acessar as rotas protegidas."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def usd(value):
    """Formata valores numéricos como moeda (USD)."""
    return f"${value:,.2f}"


def get_portfolio_metrics(tickers, weights, risk_free_rate=0.1075, period="1y"):
    """Calcula o Retorno, Volatilidade, Índice de Sharpe e VaR Histórico."""
    df = yf.download(tickers, period=period, progress=False)

    # Seleciona 'Close' ou 'Adj Close'
    if "Close" in df:
        data = df["Close"]
    elif "Adj Close" in df:
        data = df["Adj Close"]
    else:
        data = df

    # Trata dados ausentes
    data = data.dropna(how="all").ffill().bfill()

    # Cálculo dos retornos diários
    returns = data.pct_change().dropna()
    w = np.array(weights)

    # 1. Retorno Anualizado
    portfolio_return = np.sum(returns.mean() * w) * 252

    # 2. Volatilidade Anualizada
    cov_matrix = returns.cov() * 252
    portfolio_volatility = np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))

    # 3. Índice de Sharpe
    sharpe_ratio = (
        (portfolio_return - risk_free_rate) / portfolio_volatility
        if portfolio_volatility != 0
        else 0
    )

    # 4. VaR Histórico (95% de confiança diário)
    portfolio_daily_returns = (returns * w).sum(axis=1)
    var_95 = np.percentile(portfolio_daily_returns, 5)

    return {
        "return": round(portfolio_return * 100, 2),
        "volatility": round(portfolio_volatility * 100, 2),
        "sharpe": round(sharpe_ratio, 2),
        "var_95": round(var_95 * 100, 2),
    }
