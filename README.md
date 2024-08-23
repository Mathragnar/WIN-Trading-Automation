# Automated Trading System for B3 Futures Market (WIN)

## Project Description

This project is an advanced automated trading system designed for the B3 futures market, specifically targeting the WIN (Mini Ibovespa Futures) asset. It combines Python programming, machine learning, and statistical analysis to create a sophisticated trading engine.

## Key Features

- Custom machine learning model for market prediction
- Object-Oriented Programming (OOP) based system architecture
- Statistical analysis for trend identification
- Feature engineering from financial data
- Multiple algorithmic trading strategies
- Risk management techniques
- Backtesting framework and strategy optimization
- Performance monitoring dashboard

## Requirements

To run this project, you need Python 3.8+ and the following packages:

Here's a README.md for your GitHub project:
markdownCopy# Automated Trading System for B3 Futures Market (WIN)

## Project Description

This project is an advanced automated trading system designed for the B3 futures market, specifically targeting the WIN (Mini Ibovespa Futures) asset. It combines Python programming, machine learning, and statistical analysis to create a sophisticated trading engine.

## Key Features

- Custom machine learning model for market prediction
- Object-Oriented Programming (OOP) based system architecture
- Statistical analysis for trend identification
- Feature engineering from financial data
- Multiple algorithmic trading strategies
- Risk management techniques
- Backtesting framework and strategy optimization
- Performance monitoring dashboard

## Requirements

To run this project, you need Python 3.8+ and the following packages:
colorama==0.4.6
et-xmlfile==1.1.0
joblib==1.4.2
markdown-it-py==3.0.0
mdurl==0.1.2
MetaTrader5==5.0.4424
numpy==1.26.4
openpyxl==3.1.5
pandas==2.2.2
Pygments==2.18.0
python-dateutil==2.9.0.post0
pytz==2024.1
scikit-learn==1.5.1
scipy==1.14.0
six==1.16.0
threadpoolctl==3.5.0
tzdata==2024.1

You can install these dependencies using:
pip install -r requirements.txt

## Installation

1. Clone this repository:
https://github.com/Mathragnar/WIN-Trading-Automation.git

2. Navigate to the project directory:
cd b3-futures-trading-system

3. Install the required packages:
pip install -r requirements.txt

## Usage

## Usage

To run the trading system:

1. Open a terminal in the project directory.

2. Run the main script:
python Classe_Central.py

3. The system will prompt you for two inputs:
- Take Profit: Enter a positive value (e.g., 2000)
- Stop Loss: Enter a negative value (e.g., -2000)

4. After inputting these values, the system will start executing trades automatically.

Important notes:
- The system operates between 9:08 AM and 6:20 PM (18:20).
- Ensure that you have a stable internet connection and that your B3 market data feed is active during operation hours.
- Monitor the system periodically to ensure it's functioning as expected.

Remember to review and adjust your Take Profit and Stop Loss values based on your risk tolerance and market conditions. Always use this system responsibly and be aware of the risks involved in automated trading.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License
This project is proprietary and confidential. Unauthorized copying, modification, distribution, or use of this software is strictly prohibited.

## Disclaimer

This trading system is for educational and research purposes only. Always understand the risks involved in algorithmic trading and use at your own risk.
