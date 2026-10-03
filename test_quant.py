import numpy as np
import pandas as pd
import yfinance as yf

print("1. Baixando dados do Yahoo Finance...")
tickers = ["PETR4.SA", "VALE3.SA", "AAPL"]
weights = [0.4, 0.3, 0.3]

try:
    # Baixa os dados sem travar no terminal
    df = yf.download(tickers, period="1y", progress=False)

    # Suporta versões novas e antigas do yfinance
    if "Close" in df:
        data = df["Close"]
    elif "Adj Close" in df:
        data = df["Adj Close"]
    else:
        data = df

    # Trata valores ausentes
    data = data.dropna(how="all").ffill().bfill()

    # Cálculo dos retornos e métricas de risco
    returns = data.pct_change().dropna()
    w = np.array(weights)

    retorno_anual = np.sum(returns.mean() * w) * 252 * 100
    cov_matrix = returns.cov() * 252
    volatilidade = np.sqrt(np.dot(w.T, np.dot(cov_matrix, w))) * 100

    # Taxa livre de risco (Selic ~ 10.75%)
    sharpe = (retorno_anual - 10.75) / volatilidade if volatilidade != 0 else 0
    var_95 = np.percentile((returns * w).sum(axis=1), 5) * 100

    print("\n=== RESULTADOS DA ANÁLISE ===")
    print(f"Retorno Esperado: {retorno_anual:.2f}%")
    print(f"Volatilidade:     {volatilidade:.2f}%")
    print(f"Índice Sharpe:    {sharpe:.2f}")
    print(f"VaR 95% Diário:   {var_95:.2f}%")

except Exception as e:
    print(f"Erro ao buscar dados: {e}")
