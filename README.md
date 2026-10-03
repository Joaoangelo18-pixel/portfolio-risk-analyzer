# PORTFOLIO RISK ANALYZER
#### Video Demo: <https://www.youtube.com/watch?v=r7IMizlToVE&t=7s>

#### Description:
The **Portfolio Risk Analyzer** is a web-based financial analytics application designed to help investors evaluate and quantify the risk and performance metrics of custom stock portfolios. Developed as the final project for CS50x, this application leverages Python, Flask, SQLite, and quantitative finance techniques to provide clear, actionable financial metrics including Expected Return, Volatility, Sharpe Ratio, and Value at Risk (VaR 95%).

### Features and Financial Metrics
- **Portfolio Management**: Allows users to register accounts, log in, and manage stock tickers alongside their respective portfolio weights.
- **Expected Return**: Computes historical annualized expected returns based on adjusted daily closing prices retrieved via `yfinance`.
- **Volatility (Standard Deviation)**: Measures overall portfolio risk by calculating annualized standard deviation of daily returns.
- **Sharpe Ratio**: Assesses risk-adjusted returns by evaluating excess portfolio returns relative to total volatility.
- **Value at Risk (VaR 95%)**: Estimates the maximum statistical loss expected at a 95% confidence interval over a given time horizon.

### Project Structure and File Breakdown
- **`app.py`**: The main Flask application controller. Handles routing for user authentication (`/login`, `/register`, `/logout`), portfolio management, database transactions, and dashboard rendering.
- **`helpers.py`**: Contains core utility functions, including data fetching logic with `yfinance`, mathematical computations using `pandas` and `numpy`, Jinja currency formatting filters, and session login decorators.
- **`project.db`**: SQLite database storing persistent user credential hashes and saved portfolio allocation data.
- **`templates/`**: Contains HTML templates using Jinja2 syntax, including `layout.html`, `login.html`, `register.html`, and `index.html` for presenting tabular analytical results.

### Design Decisions
A modular approach was chosen to separate financial calculations from route handlers, isolating algorithmic logic within `helpers.py`. SQLite was selected for lightweight, serverless persistence. Pandas and NumPy were implemented to ensure efficient vectorized operations on historical return matrices.
