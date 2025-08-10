# 📈 Real-Time Stock Market Dashboard

A comprehensive, real-time stock market dashboard built with Python, Streamlit, and Plotly that provides live stock data visualization, technical indicators, and market analysis.

## 🚀 Features

### 📊 Real-Time Data
- Live stock price updates using Yahoo Finance API
- Real-time market indices (S&P 500, Dow Jones, NASDAQ, VIX)
- Auto-refresh functionality (30-second intervals)

### 📈 Advanced Charts & Indicators
- **Candlestick Charts**: OHLC price visualization
- **Technical Indicators**:
  - Moving Averages (20-day and 50-day)
  - Relative Strength Index (RSI)
  - Bollinger Bands
- **Volume Analysis**: Trading volume with color-coded bars
- **Interactive Charts**: Zoom, pan, and hover functionality

### 💼 Portfolio Management
- Multi-stock portfolio tracking
- Performance comparison charts
- Portfolio summary with key metrics
- Market sentiment analysis

### 📋 Market Analysis
- Market overview with major indices
- Sentiment distribution (Bullish/Bearish)
- 52-week high/low tracking
- Price change percentage calculations

## 🛠️ Technologies Used

- **Python 3.8+**
- **Streamlit**: Web application framework
- **Plotly**: Interactive data visualization
- **Pandas**: Data manipulation and analysis
- **yfinance**: Yahoo Finance API wrapper
- **Requests**: HTTP library for API calls

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Real-time-stock-market-dashboard
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

1. **Run the application**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**
   - The dashboard will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, navigate to the URL manually

3. **Using the Dashboard**
   - **Select Stocks**: Choose from popular stocks in the sidebar
   - **Time Period**: Select different time ranges (1D to 5Y)
   - **Auto-refresh**: Toggle automatic data updates
   - **Navigate Tabs**: Switch between different views

## 📊 Dashboard Sections

### 1. Stock Charts Tab
- Individual stock analysis with technical indicators
- Real-time price metrics
- Interactive candlestick charts
- Volume and RSI analysis

### 2. Portfolio Overview Tab
- Multi-stock portfolio summary
- Performance comparison charts
- Portfolio metrics table
- Normalized performance visualization

### 3. Market Summary Tab
- Major market indices overview
- Market sentiment analysis
- Real-time market data
- Sentiment distribution charts

## 🎯 Supported Stocks

The dashboard includes popular stocks by default:
- **AAPL** - Apple Inc.
- **GOOGL** - Alphabet Inc.
- **MSFT** - Microsoft Corporation
- **AMZN** - Amazon.com Inc.
- **TSLA** - Tesla Inc.
- **META** - Meta Platforms Inc.
- **NVDA** - NVIDIA Corporation
- **NFLX** - Netflix Inc.
- **JPM** - JPMorgan Chase & Co.
- **JNJ** - Johnson & Johnson

## 📈 Technical Indicators Explained

### Moving Averages (MA)
- **MA20**: 20-day moving average - short-term trend indicator
- **MA50**: 50-day moving average - medium-term trend indicator

### Relative Strength Index (RSI)
- Momentum oscillator measuring speed and magnitude of price changes
- Values above 70 indicate overbought conditions
- Values below 30 indicate oversold conditions

### Bollinger Bands
- Volatility indicator showing upper and lower bands
- Price near upper band may indicate overbought
- Price near lower band may indicate oversold

## 🔧 Configuration

### Customizing Stock List
Edit the `popular_stocks` dictionary in `app.py` to add or remove stocks:

```python
popular_stocks = {
    "AAPL": "Apple Inc.",
    "GOOGL": "Alphabet Inc.",
    # Add your preferred stocks here
}
```

### Auto-refresh Settings
Modify the refresh interval by changing the `time.sleep(30)` value in the auto-refresh section.

## 📱 Features

- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Updates**: Live data with configurable refresh rates
- **Interactive Charts**: Zoom, pan, and hover for detailed analysis
- **Professional UI**: Clean, modern interface with custom styling
- **Error Handling**: Graceful handling of API failures and data issues

## 🚨 Important Notes

- **Market Hours**: Data availability depends on market hours
- **API Limits**: Yahoo Finance API has rate limits
- **Data Accuracy**: Data is provided by Yahoo Finance and may have delays
- **Internet Connection**: Requires stable internet connection for real-time data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Yahoo Finance**: For providing free stock market data
- **Streamlit**: For the excellent web app framework
- **Plotly**: For interactive charting capabilities
- **Pandas**: For powerful data manipulation tools

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section below
2. Open an issue on GitHub
3. Review the documentation

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Data Not Loading**
   - Check internet connection
   - Verify stock symbols are correct
   - Check if markets are open

3. **Performance Issues**
   - Reduce number of selected stocks
   - Increase refresh interval
   - Close other applications

4. **Chart Display Issues**
   - Clear browser cache
   - Try different browser
   - Check browser console for errors

---

**Happy Trading! 📈💰**
