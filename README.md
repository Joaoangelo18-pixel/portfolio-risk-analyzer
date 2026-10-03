# PORTFOLIO RISK ANALYZER
#### Video Demo: <https://www.youtube.com/watch?v=r7IMizlToVE&t=7s>

#### Description:
The **Portfolio Risk Analyzer** is a full-stack web application designed to help individual investors, financial analysts, and retail traders evaluate, quantify, and visualize quantitative risk and performance metrics for custom stock portfolios. Developed as the final project for CS50x, the application bridges the gap between complex quantitative finance methodologies and user-friendly web software, utilizing Python, Flask, SQLite, Pandas, NumPy, and `yfinance`.

### Background and Motivation
Modern Portfolio Theory emphasizes that an investment's risk and return should not be assessed in isolation, but by how the asset contributes to an overall portfolio's risk and reward profile. Many novice investors focus solely on potential returns without understanding downside exposure, portfolio variance, or statistical risk limits.

The **Portfolio Risk Analyzer** solves this problem by allowing users to build a custom portfolio of publicly traded equities, assign allocation weights, and instantly compute institutional-grade risk metrics derived from historical market data.

---

### Core Financial Metrics Calculated

1. **Expected Return (Annualized)**: Calculated by computing the daily log or percentage returns of the selected assets, taking the weighted average daily return across the portfolio, and annualizing the result assuming 252 trading days in a standard calendar year.
2. **Portfolio Volatility (Standard Deviation)**: Measures the total dispersion of portfolio returns relative to its mean. The calculation utilizes covariance matrices between asset daily returns to account for inter-asset correlation, scaled by the square root of 252 for annualization.
3. **Sharpe Ratio**: Assesses risk-adjusted performance by calculating the excess portfolio return per unit of total risk (volatility). A higher Sharpe Ratio indicates superior risk-adjusted returns relative to a risk-free benchmark.
4. **Value at Risk (VaR 95%)**: Represents the maximum expected statistical loss over a single trading day at a 95% confidence level. Calculated using historical simulation and parametric variance-covariance techniques, giving users a clear threshold of potential downside loss under normal market conditions.

---

### Application Architecture and Workflow

The application follows the Model-View-Controller (MVC) architectural pattern:

- **Authentication & User Management**: Users can register for an account, log in securely using password hashing, and manage their personal session state.
- **Portfolio Input Interface**: Users enter stock tickers (e.g., AAPL, MSFT, GOOGL, NVDA) along with their respective percentage weights. The frontend validates that the total weight sum equals 100% before submission.
- **Data Ingestion & Quantitative Processing**: Upon form submission, the backend issues asynchronous requests via `yfinance` to download historical daily closing prices over a default lookback period (e.g., 1 to 3 years). Pandas and NumPy execute matrix operations to generate returns, covariances, standard deviations, and statistical quantiles.
- **Dashboard & Analytical Visualization**: Results are rendered dynamically using Jinja2 templates, presenting key statistics in clean summary cards and tabular formats.

---

### File Breakdown

- **`app.py`**: Serves as the primary HTTP request router and application controller. Configures Flask, manages session storage, sets up database connections using the CS50 SQL wrapper, defines authentication routes (`/login`, `/register`, `/logout`), and handles POST requests for portfolio risk computations.
- **`helpers.py`**: Contains core utility and mathematical processing functions. Implements data retrieval wrappers around `yfinance`, statistical formulas for expected return, variance-covariance calculations, Sharpe ratio evaluation, and VaR estimation. Also includes custom Jinja formatting filters (such as USD currency formatting) and the `@login_required` decorator.
- **`project.db`**: SQLite database storing persistent user credential hashes, saved portfolios, user asset holdings, and portfolio execution history.
- **`templates/`**:
  - **`layout.html`**: The master HTML layout template featuring navigation bars, flash messaging containers, and Bootstrap styling links.
  - **`index.html`**: The main user dashboard where users configure asset allocations and view calculated risk metrics.
  - **`login.html` & `register.html`**: Simple, intuitive forms for authentication and account registration with client-side and server-side validation.
  - **`apology.html`**: Error-handling template that displays custom error messages and HTTP status codes to users when invalid tickers or bad allocations are submitted.
- **`static/`**: Contains custom CSS styling, design tweaks, and asset files to ensure a responsive and polished modern presentation.
- **`requirements.txt`**: Lists all third-party Python library dependencies including `Flask`, `Flask-Session`, `cs50`, `pandas`, `numpy`, and `yfinance`.

---

### Design Decisions and Engineering Trade-offs

- **Pandas/NumPy vs. Pure Python**: Using standard Python lists and loops for covariance matrices and historical asset returns would have resulted in slow execution times and verbose code. Leveraging Pandas DataFrames and NumPy array operations provided massive performance gains through vectorized matrix math.
- **`yfinance` API Ingestion**: Direct REST queries to market data providers often require paid API keys and strict rate limits. `yfinance` was selected as a robust, open-source solution to fetch accurate market data directly into Pandas structures.
- **SQLite Database**: SQLite was chosen for its lightweight, zero-configuration architecture, making it seamless to run within the CS50 Codespace environment without requiring an external database server like PostgreSQL or MySQL.
- **Input Validation & Edge Cases**: Significant design effort went into handling real-world market data edge cases, such as invalid stock tickers, mismatched historical dates across assets, zero-division in Sharpe ratio calculations when volatility is zero, and unallocated portfolio weights.

---

### Conclusion and Future Enhancements
The **Portfolio Risk Analyzer** provides an accessible yet mathematically rigorous tool for portfolio evaluation. Future improvements include adding interactive price charts using Chart.js, integrating real-time market data websockets, supporting multi-asset classes like ETFs and cryptocurrencies, and adding Monte Carlo simulations for long-term portfolio forecasting.
