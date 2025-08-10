# Configuration file for Real-Time Stock Market Dashboard

# Dashboard Settings
DASHBOARD_CONFIG = {
    "page_title": "Real-Time Stock Market Dashboard",
    "page_icon": "📈",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Auto-refresh settings
AUTO_REFRESH_CONFIG = {
    "default_interval": 30,  # seconds
    "enabled_by_default": True
}

# Chart settings
CHART_CONFIG = {
    "height": 800,
    "template": "plotly_white",
    "show_legend": True
}

# Technical indicators settings
INDICATORS_CONFIG = {
    "ma_short": 20,  # Short-term moving average
    "ma_long": 50,   # Long-term moving average
    "rsi_period": 14,  # RSI calculation period
    "bb_period": 20,   # Bollinger Bands period
    "bb_std": 2        # Bollinger Bands standard deviation
}

# Popular stocks with company names
POPULAR_STOCKS = {
    "AAPL": "Apple Inc.",
    "GOOGL": "Alphabet Inc.",
    "MSFT": "Microsoft Corporation",
    "AMZN": "Amazon.com Inc.",
    "TSLA": "Tesla Inc.",
    "META": "Meta Platforms Inc.",
    "NVDA": "NVIDIA Corporation",
    "NFLX": "Netflix Inc.",
    "JPM": "JPMorgan Chase & Co.",
    "JNJ": "Johnson & Johnson",
    "V": "Visa Inc.",
    "WMT": "Walmart Inc.",
    "PG": "Procter & Gamble Co.",
    "UNH": "UnitedHealth Group Inc.",
    "HD": "Home Depot Inc.",
    "MA": "Mastercard Inc.",
    "DIS": "Walt Disney Co.",
    "PYPL": "PayPal Holdings Inc.",
    "BAC": "Bank of America Corp.",
    "ADBE": "Adobe Inc.",
    "WAAENERGIES.NS": "Waaree Energies Ltd. (India)",
    "CRESTCHM.NS": "Crestchem Ltd. (India)"
}

# Market indices
MARKET_INDICES = {
    "^GSPC": "S&P 500",
    "^DJI": "Dow Jones Industrial Average",
    "^IXIC": "NASDAQ Composite",
    "^VIX": "VIX Volatility Index",
    "^RUT": "Russell 2000",
    "^FTSE": "FTSE 100"
}

# Time periods for data fetching
TIME_PERIODS = {
    "1D": "1 day",
    "5D": "5 days",
    "1M": "1 month",
    "3M": "3 months",
    "6M": "6 months",
    "1Y": "1 year",
    "2Y": "2 years",
    "5Y": "5 years"
}

# Color schemes
COLORS = {
    "positive": "#00ff00",
    "negative": "#ff0000",
    "neutral": "#1f77b4",
    "background": "#f0f2f6",
    "text": "#333333"
}

# API settings
API_CONFIG = {
    "cache_ttl": 30,  # Cache time-to-live in seconds
    "max_retries": 3,
    "timeout": 10
}
