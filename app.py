import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
import time
from datetime import datetime, timedelta
import json
from bs4 import BeautifulSoup
import re

# Page configuration
st.set_page_config(
    page_title="Real-Time Stock Market Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme selection with more options
st.sidebar.markdown("---")
st.sidebar.subheader("🎨 Theme Settings")

theme_mode = st.sidebar.selectbox(
    "Choose Theme",
    ["Light", "Dark", "Sepia", "Ocean Blue", "Forest Green", "Sunset Orange", "Purple Night"],
    index=0
)

# Theme preview
theme_colors = {
    "Light": {"primary": "#1f77b4", "bg": "#ffffff", "text": "#000000"},
    "Dark": {"primary": "#4CAF50", "bg": "#1a202c", "text": "#ffffff"},
    "Sepia": {"primary": "#8B4513", "bg": "#faf8f3", "text": "#3e2723"},
    "Ocean Blue": {"primary": "#0066cc", "bg": "#e6f3ff", "text": "#003366"},
    "Forest Green": {"primary": "#2d5016", "bg": "#f0f8f0", "text": "#1a3310"},
    "Sunset Orange": {"primary": "#ff6b35", "bg": "#fff5f0", "text": "#8b4513"},
    "Purple Night": {"primary": "#9c27b0", "bg": "#f3e5f5", "text": "#4a148c"}
}

# Show theme preview
selected_color = theme_colors[theme_mode]
st.sidebar.markdown(f"""
<div style="
    background-color: {selected_color['bg']}; 
    color: {selected_color['text']}; 
    padding: 10px; 
    border-radius: 5px; 
    border-left: 4px solid {selected_color['primary']};
    margin: 10px 0;
">
    <strong>🎨 {theme_mode} Theme</strong><br>
    <small>Primary: {selected_color['primary']}</small>
</div>
""", unsafe_allow_html=True)

# Theme information
with st.sidebar.expander("ℹ️ Theme Information"):
    st.markdown("""
    **Available Themes:**
    - **Light**: Classic blue theme
    - **Dark**: Green accents on dark background
    - **Sepia**: Warm brown tones
    - **Ocean Blue**: Cool blue palette
    - **Forest Green**: Natural green theme
    - **Sunset Orange**: Warm orange tones
    - **Purple Night**: Elegant purple theme
    
    *Charts will automatically adapt to your selected theme!*
    """)

# Custom CSS for different themes
def get_theme_css(theme):
    themes = {
        "Light": {
            "header_color": "#1f77b4",
            "bg_color": "#ffffff",
            "text_color": "#000000",
            "sidebar_bg": "#f0f2f6",
            "card_bg": "#f0f2f6",
            "positive_color": "#00ff00",
            "negative_color": "#ff0000",
            "tab_bg": "#f0f2f6",
            "tab_selected": "#1f77b4"
        },
        "Dark": {
            "header_color": "#4CAF50",
            "bg_color": "#1a202c",
            "text_color": "#ffffff",
            "sidebar_bg": "#2d3748",
            "card_bg": "#2d3748",
            "positive_color": "#4CAF50",
            "negative_color": "#f56565",
            "tab_bg": "#4a5568",
            "tab_selected": "#4CAF50"
        },
        "Sepia": {
            "header_color": "#8B4513",
            "bg_color": "#faf8f3",
            "text_color": "#3e2723",
            "sidebar_bg": "#f5f1e8",
            "card_bg": "#f5f1e8",
            "positive_color": "#2e7d32",
            "negative_color": "#c62828",
            "tab_bg": "#e8dcc0",
            "tab_selected": "#8B4513"
        },
        "Ocean Blue": {
            "header_color": "#0066cc",
            "bg_color": "#e6f3ff",
            "text_color": "#003366",
            "sidebar_bg": "#cce7ff",
            "card_bg": "#cce7ff",
            "positive_color": "#0066cc",
            "negative_color": "#cc0000",
            "tab_bg": "#b3d9ff",
            "tab_selected": "#0066cc"
        },
        "Forest Green": {
            "header_color": "#2d5016",
            "bg_color": "#f0f8f0",
            "text_color": "#1a3310",
            "sidebar_bg": "#e0f0e0",
            "card_bg": "#e0f0e0",
            "positive_color": "#2d5016",
            "negative_color": "#8b0000",
            "tab_bg": "#d0e8d0",
            "tab_selected": "#2d5016"
        },
        "Sunset Orange": {
            "header_color": "#ff6b35",
            "bg_color": "#fff5f0",
            "text_color": "#8b4513",
            "sidebar_bg": "#ffe8e0",
            "card_bg": "#ffe8e0",
            "positive_color": "#ff6b35",
            "negative_color": "#cc3300",
            "tab_bg": "#ffd6c0",
            "tab_selected": "#ff6b35"
        },
        "Purple Night": {
            "header_color": "#9c27b0",
            "bg_color": "#f3e5f5",
            "text_color": "#4a148c",
            "sidebar_bg": "#e8d4f0",
            "card_bg": "#e8d4f0",
            "positive_color": "#9c27b0",
            "negative_color": "#d32f2f",
            "tab_bg": "#d8b8e8",
            "tab_selected": "#9c27b0"
        }
    }
    
    colors = themes.get(theme, themes["Light"])
    
    return f"""
    <style>
        .main-header {{
            font-size: 3rem;
            font-weight: bold;
            color: {colors['header_color']};
            text-align: center;
            margin-bottom: 2rem;
        }}
        .metric-card {{
            background-color: {colors['card_bg']};
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid {colors['header_color']};
            color: {colors['text_color']};
        }}
        .positive-change {{
            color: {colors['positive_color']};
            font-weight: bold;
        }}
        .negative-change {{
            color: {colors['negative_color']};
            font-weight: bold;
        }}
        .stApp {{
            background-color: {colors['bg_color']};
            color: {colors['text_color']};
        }}
        .stSidebar {{
            background-color: {colors['sidebar_bg']};
            color: {colors['text_color']};
        }}
        .stTabs [data-baseweb="tab-list"] {{
            background-color: {colors['sidebar_bg']};
        }}
        .stTabs [data-baseweb="tab"] {{
            background-color: {colors['tab_bg']};
            color: {colors['text_color']};
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {colors['tab_selected']};
            color: white;
        }}
    </style>
    """

# Apply theme CSS
st.markdown(get_theme_css(theme_mode), unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📈 Real-Time Stock Market Dashboard</h1>', unsafe_allow_html=True)

# Sidebar for stock selection
st.sidebar.header("📊 Stock Selection")
st.sidebar.markdown("---")

# Popular Indian stocks list
popular_stocks = {
    "RELIANCE": "Reliance Industries Ltd. (NSE)",
    "TCS": "Tata Consultancy Services Ltd. (NSE)",
    "INFY": "Infosys Ltd. (NSE)",
    "HDFCBANK": "HDFC Bank Ltd. (NSE)",
    "ICICIBANK": "ICICI Bank Ltd. (NSE)",
    "SBIN": "State Bank of India (NSE)",
    "BHARTIARTL": "Bharti Airtel Ltd. (NSE)",
    "ITC": "ITC Ltd. (NSE)",
    "KOTAKBANK": "Kotak Mahindra Bank Ltd. (NSE)",
    "AXISBANK": "Axis Bank Ltd. (NSE)",
    "ASIANPAINT": "Asian Paints Ltd. (NSE)",
    "MARUTI": "Maruti Suzuki India Ltd. (NSE)",
    "WAAENERGIES": "Waaree Energies Ltd. (NSE)",
    "CRESTCHM": "Crestchem Ltd. (NSE)",
    "TATAMOTORS": "Tata Motors Ltd. (NSE)",
    "HINDUNILVR": "Hindustan Unilever Ltd. (NSE)",
    "SUNPHARMA": "Sun Pharmaceutical Industries Ltd. (NSE)",
    "ULTRACEMCO": "UltraTech Cement Ltd. (NSE)",
    "TITAN": "Titan Company Ltd. (NSE)"
}

# Stock selection
selected_stocks = st.sidebar.multiselect(
    "Select Indian stocks to track:",
    options=list(popular_stocks.keys()),
    default=["RELIANCE"],  # Start with Reliance Industries
    format_func=lambda x: f"{x} - {popular_stocks[x]}"
)

# Time period selection
time_period = st.sidebar.selectbox(
    "Select time period:",
    ["1D", "5D", "1M", "3M", "6M", "1Y", "2Y", "5Y"],
    index=2
)

# Auto-refresh toggle
auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (30s)", value=True)

# Sample data toggle for testing
use_sample_data = st.sidebar.checkbox("🧪 Use Sample Data (recommended)", value=True)
if use_sample_data:
    st.sidebar.success("📊 Using sample data - all features will work!")
else:
    st.sidebar.warning("⚠️ Real data may not work due to API issues")
    st.warning("⚠️ **API Notice**: Yahoo Finance API is currently experiencing issues. For the best experience, enable 'Use Sample Data' in the sidebar.")

# Rate limiting warning
st.sidebar.markdown("---")
st.sidebar.warning("⚠️ **Rate Limiting Notice**\n\nTo avoid API limits, please:\n• Select fewer stocks (max 3-4)\n• Use longer refresh intervals\n• Be patient with data loading")

# Test API connection
if st.sidebar.button("🔍 Test Indian Market APIs"):
    try:
        # Test NSE API
        test_symbol = "RELIANCE"
        st.sidebar.info("🔄 Testing NSE API...")
        
        nse_data, _ = get_nse_data(test_symbol, "5d")
        if nse_data is not None and not nse_data.empty:
            st.sidebar.success(f"✅ NSE API working with {test_symbol}!")
            st.sidebar.info(f"Latest {test_symbol} price: ₹{nse_data['Close'].iloc[-1]:.2f}")
        else:
            st.sidebar.warning("⚠️ NSE API test failed")
            
        # Test BSE API
        st.sidebar.info("🔄 Testing BSE API...")
        bse_data, _ = get_bse_data(test_symbol, "5d")
        if bse_data is not None and not bse_data.empty:
            st.sidebar.success(f"✅ BSE API working with {test_symbol}!")
            st.sidebar.info(f"Latest {test_symbol} price: ₹{bse_data['Close'].iloc[-1]:.2f}")
        else:
            st.sidebar.warning("⚠️ BSE API test failed")
            
        st.sidebar.info("💡 Use 'Sample Data' mode for testing if APIs fail")
            
    except Exception as e:
        st.sidebar.error(f"❌ API connection failed: {str(e)}")
        st.sidebar.info("💡 Use 'Sample Data' mode for testing the dashboard")

# Function to get stock symbol with proper exchange suffix
def get_stock_symbol(symbol):
    """Add proper exchange suffix if needed"""
    if symbol.endswith('.NS'):
        return symbol  # Already has NSE suffix
    elif symbol.endswith('.BO'):
        return symbol  # Already has BSE suffix
    else:
        # For US stocks, no suffix needed
        return symbol

# Function to validate Indian stock symbols
def validate_indian_stock(symbol):
    """Validate and suggest corrections for Indian stock symbols"""
    indian_stocks = {
        "WAAENERGIES": "WAAENERGIES.NS",
        "CRESTCHM": "CRESTCHM.NS",
        "RELIANCE": "RELIANCE.NS",
        "TCS": "TCS.NS",
        "INFY": "INFY.NS",
        "HDFCBANK": "HDFCBANK.NS",
        "ICICIBANK": "ICICIBANK.NS",
        "SBIN": "SBIN.NS",
        "BHARTIARTL": "BHARTIARTL.NS",
        "ITC": "ITC.NS"
    }
    
    if symbol in indian_stocks:
        return indian_stocks[symbol]
    return symbol

# Function to test stock symbol availability
def test_stock_symbol(symbol):
    """Test if a stock symbol is available and return suggestions"""
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d")
        if hist is not None and not hist.empty:
            return True, "Symbol is valid"
        else:
            return False, "No data available for this symbol"
    except Exception as e:
        return False, f"Error: {str(e)}"

# Function to create sample data for testing
def create_sample_data(symbol):
    """Create sample data for testing when API fails"""
    import pandas as pd
    import random
    from datetime import datetime, timedelta
    
    # Create sample data for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Set seed for consistent data
    random.seed(hash(symbol) % 1000)
    
    # Generate sample price data based on Indian stock symbols
    if symbol == "RELIANCE":
        base_price = 2500.0
        trend = 0.3
    elif symbol == "TCS":
        base_price = 3500.0
        trend = 0.2
    elif symbol == "INFY":
        base_price = 1500.0
        trend = 0.15
    elif symbol == "HDFCBANK":
        base_price = 1600.0
        trend = 0.1
    elif symbol == "ICICIBANK":
        base_price = 900.0
        trend = 0.2
    elif symbol == "SBIN":
        base_price = 600.0
        trend = 0.25
    elif symbol == "BHARTIARTL":
        base_price = 800.0
        trend = 0.1
    elif symbol == "ITC":
        base_price = 400.0
        trend = 0.05
    elif symbol == "WAAENERGIES":
        base_price = 1200.0
        trend = 0.4
    elif symbol == "CRESTCHM":
        base_price = 80.0
        trend = 0.15
    else:
        base_price = 500.0
        trend = 0.1
    
    prices = []
    current_price = base_price
    
    for i in range(len(dates)):
        # Add trend and random variation
        daily_change = random.uniform(-3, 3) + trend
        current_price = max(current_price + daily_change, 1.0)  # Ensure price is positive
        prices.append(current_price)
    
    # Create DataFrame with realistic OHLC data
    data = {
        'Open': [],
        'High': [],
        'Low': [],
        'Close': prices,
        'Volume': []
    }
    
    for i, close_price in enumerate(prices):
        # Generate realistic OHLC
        daily_range = random.uniform(2, 8)
        open_price = close_price + random.uniform(-daily_range/2, daily_range/2)
        high_price = max(open_price, close_price) + random.uniform(0, daily_range/2)
        low_price = min(open_price, close_price) - random.uniform(0, daily_range/2)
        
        data['Open'].append(open_price)
        data['High'].append(high_price)
        data['Low'].append(low_price)
        data['Volume'].append(random.randint(1000000, 8000000))
    
    df = pd.DataFrame(data, index=dates)
    return df

# Function to get NSE data
def get_nse_data(symbol, period="1mo"):
    """Fetch data from NSE using nsepy"""
    try:
        from nsepy import get_history
        from datetime import date
        
        # Remove .NS suffix if present
        clean_symbol = symbol.replace('.NS', '')
        
        # Calculate date range
        end_date = date.today()
        if period == "1d":
            start_date = end_date
        elif period == "5d":
            start_date = end_date - timedelta(days=5)
        elif period == "1mo":
            start_date = end_date - timedelta(days=30)
        elif period == "3mo":
            start_date = end_date - timedelta(days=90)
        else:
            start_date = end_date - timedelta(days=30)
        
        # Fetch data from NSE
        data = get_history(symbol=clean_symbol, start=start_date, end=end_date)
        
        if data is not None and not data.empty:
            st.success(f"✅ NSE data fetched for {symbol}")
            return data, {}
        else:
            return None, {}
            
    except Exception as e:
        st.warning(f"NSE data fetch failed for {symbol}: {str(e)}")
        return None, {}

# Function to get BSE data
def get_bse_data(symbol, period="1mo"):
    """Fetch data from BSE using web scraping"""
    try:
        # Remove .BO suffix if present
        clean_symbol = symbol.replace('.BO', '')
        
        # BSE URL for stock data
        url = f"https://www.bseindia.com/stock-share-price/{clean_symbol}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract price data (this is a simplified version)
            # In a real implementation, you'd need to parse the specific BSE page structure
            
            # For now, return None as BSE scraping requires more complex implementation
            return None, {}
        else:
            return None, {}
            
    except Exception as e:
        st.warning(f"BSE data fetch failed for {symbol}: {str(e)}")
        return None, {}

# Function to get TradingView data (simplified)
def get_tradingview_data(symbol, period="1mo"):
    """Fetch data from TradingView (simplified implementation)"""
    try:
        # TradingView API requires authentication and is complex
        # This is a placeholder for future implementation
        
        # For now, return None
        return None, {}
        
    except Exception as e:
        st.warning(f"TradingView data fetch failed for {symbol}: {str(e)}")
        return None, {}

# Function to get data from multiple sources
def get_multi_source_data(symbol, period="1mo"):
    """Try multiple data sources in order of preference"""
    
    # For Indian stocks, try NSE first, then BSE
    sources = [
        ("NSE", lambda: get_nse_data(symbol, period)),
        ("BSE", lambda: get_bse_data(symbol, period))
    ]
    
    for source_name, source_func in sources:
        try:
            st.info(f"🔄 Trying {source_name} for {symbol}...")
            data, info = source_func()
            
            if data is not None and not data.empty:
                st.success(f"✅ Data fetched from {source_name} for {symbol}")
                return data, info
                
        except Exception as e:
            st.warning(f"❌ {source_name} failed for {symbol}: {str(e)}")
            continue
    
    st.error(f"❌ All data sources failed for {symbol}")
    return None, {}

# Function to get stock data with improved error handling
@st.cache_data(ttl=300)  # Increased cache time to reduce API calls
def get_stock_data(symbol, period="1mo"):
    """Fetch stock data from Indian market sources"""
    
    # Check if sample data is requested
    if use_sample_data:
        return create_sample_data(symbol), {}
    
    # Try to get data from multiple sources
    return get_multi_source_data(symbol, period)

# Function to calculate technical indicators
def calculate_indicators(df):
    """Calculate technical indicators"""
    if df is None or df.empty:
        return df
    
    # Moving averages
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    
    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Bollinger Bands
    df['BB_middle'] = df['Close'].rolling(window=20).mean()
    bb_std = df['Close'].rolling(window=20).std()
    df['BB_upper'] = df['BB_middle'] + (bb_std * 2)
    df['BB_lower'] = df['BB_middle'] - (bb_std * 2)
    
    return df

# Function to create stock chart
def create_stock_chart(df, symbol, stock_info):
    """Create comprehensive stock chart with indicators"""
    if df is None or df.empty:
        return None
    
    # Calculate indicators
    df = calculate_indicators(df)
    
    # Create subplots
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=(f'{symbol} Stock Price', 'Volume', 'RSI'),
        row_heights=[0.6, 0.2, 0.2]
    )
    
    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Price',
            increasing_line_color='#00ff00',
            decreasing_line_color='#ff0000'
        ),
        row=1, col=1
    )
    
    # Moving averages
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['MA20'],
            mode='lines',
            name='MA20',
            line=dict(color='orange', width=1)
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['MA50'],
            mode='lines',
            name='MA50',
            line=dict(color='blue', width=1)
        ),
        row=1, col=1
    )
    
    # Bollinger Bands
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['BB_upper'],
            mode='lines',
            name='BB Upper',
            line=dict(color='gray', width=1, dash='dash'),
            showlegend=False
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['BB_lower'],
            mode='lines',
            name='BB Lower',
            line=dict(color='gray', width=1, dash='dash'),
            fill='tonexty',
            fillcolor='rgba(128,128,128,0.1)',
            showlegend=False
        ),
        row=1, col=1
    )
    
    # Volume
    colors = ['red' if close < open else 'green' for close, open in zip(df['Close'], df['Open'])]
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['Volume'],
            name='Volume',
            marker_color=colors,
            opacity=0.7
        ),
        row=2, col=1
    )
    
    # RSI
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['RSI'],
            mode='lines',
            name='RSI',
            line=dict(color='purple', width=2)
        ),
        row=3, col=1
    )
    
    # RSI overbought/oversold lines
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
    
    # Update layout with theme-specific template
    company_name = popular_stocks.get(symbol, symbol)
    
    # Choose template based on theme
    if theme_mode == "Dark":
        template = "plotly_dark"
    elif theme_mode in ["Ocean Blue", "Forest Green", "Sunset Orange", "Purple Night"]:
        template = "plotly_white"  # Light templates for better readability
    else:
        template = "plotly_white"
    
    fig.update_layout(
        title=f"{symbol} - {company_name}",
        xaxis_rangeslider_visible=False,
        height=800,
        showlegend=True,
        template=template
    )
    
    return fig

# Function to create metrics cards
def create_metrics_cards(stock_data, stock_info, symbol):
    """Create metrics cards for stock information"""
    if stock_data is None or stock_data.empty:
        return
    
    current_price = stock_data['Close'].iloc[-1]
    previous_price = stock_data['Close'].iloc[-2] if len(stock_data) > 1 else current_price
    price_change = current_price - previous_price
    price_change_pct = (price_change / previous_price) * 100 if previous_price != 0 else 0
    
    # Calculate 52-week high/low from available data
    high_52w = stock_data['High'].max() if len(stock_data) > 0 else current_price
    low_52w = stock_data['Low'].min() if len(stock_data) > 0 else current_price
    
    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Current Price",
            value=f"${current_price:.2f}",
            delta=f"{price_change:.2f} ({price_change_pct:.2f}%)",
            delta_color="normal" if price_change >= 0 else "inverse"
        )
    
    with col2:
        volume = stock_data['Volume'].iloc[-1]
        st.metric(
            label="Volume",
            value=f"{volume:,.0f}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="52W High",
            value=f"${high_52w:.2f}",
            delta=None
        )
    
    with col4:
        st.metric(
            label="52W Low",
            value=f"${low_52w:.2f}",
            delta=None
        )

# Main dashboard
if selected_stocks:
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Stock Charts", "📈 Portfolio Overview", "📋 Market Summary"])
    
    with tab1:
        st.header("📊 Individual Stock Analysis")
        
        for symbol in selected_stocks:
            with st.container():
                st.markdown(f"### {symbol} - {popular_stocks.get(symbol, symbol)}")
                
                # Get stock data
                stock_data, stock_info = get_stock_data(symbol, time_period)
                
                if stock_data is not None and not stock_data.empty:
                    # Create metrics cards
                    create_metrics_cards(stock_data, stock_info, symbol)
                    
                    # Create and display chart
                    chart = create_stock_chart(stock_data, symbol, stock_info)
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)
                    
                    st.markdown("---")
                else:
                    st.error(f"Unable to fetch data for {symbol}")
    
    with tab2:
        st.header("📈 Portfolio Overview")
        
        # Create portfolio summary
        portfolio_data = []
        
        for symbol in selected_stocks:
            stock_data, stock_info = get_stock_data(symbol, "1mo")
            if stock_data is not None and not stock_data.empty:
                current_price = stock_data['Close'].iloc[-1]
                previous_price = stock_data['Close'].iloc[-2] if len(stock_data) > 1 else current_price
                price_change = current_price - previous_price
                price_change_pct = (price_change / previous_price) * 100 if previous_price != 0 else 0
                
                portfolio_data.append({
                    'Symbol': symbol,
                    'Name': popular_stocks.get(symbol, symbol),
                    'Price': current_price,
                    'Change': price_change,
                    'Change %': price_change_pct,
                    'Volume': stock_data['Volume'].iloc[-1]
                })
        
        if portfolio_data:
            df_portfolio = pd.DataFrame(portfolio_data)
            
            # Display portfolio table with fallback for styling
            try:
                st.dataframe(
                    df_portfolio.style.format({
                        'Price': '${:.2f}',
                        'Change': '${:.2f}',
                        'Change %': '{:.2f}%',
                        'Volume': '{:,.0f}'
                    }).background_gradient(subset=['Change %'], cmap='RdYlGn'),
                    use_container_width=True
                )
            except ImportError:
                # Fallback without styling if jinja2 is not available
                st.dataframe(
                    df_portfolio.round(2),
                    use_container_width=True
                )
                st.info("💡 For better formatting, ensure jinja2>=3.1.2 is installed")
            
            # Portfolio performance chart
            st.subheader("Portfolio Performance")
            
            # Create performance comparison chart
            performance_data = []
            for symbol in selected_stocks:
                stock_data, _ = get_stock_data(symbol, "1mo")
                if stock_data is not None and not stock_data.empty:
                    # Normalize to starting price
                    normalized_prices = stock_data['Close'] / stock_data['Close'].iloc[0] * 100
                    performance_data.append({
                        'Date': stock_data.index,
                        'Symbol': symbol,
                        'Performance': normalized_prices
                    })
            
            if performance_data:
                fig_performance = go.Figure()
                for data in performance_data:
                    fig_performance.add_trace(
                        go.Scatter(
                            x=data['Date'],
                            y=data['Performance'],
                            mode='lines',
                            name=data['Symbol'],
                            line=dict(width=2)
                        )
                    )
                
                # Choose template based on theme
                if theme_mode == "Dark":
                    template = "plotly_dark"
                elif theme_mode in ["Ocean Blue", "Forest Green", "Sunset Orange", "Purple Night"]:
                    template = "plotly_white"
                else:
                    template = "plotly_white"
                
                fig_performance.update_layout(
                    title="Portfolio Performance Comparison (Normalized to 100)",
                    xaxis_title="Date",
                    yaxis_title="Performance (%)",
                    template=template
                )
                
                st.plotly_chart(fig_performance, use_container_width=True)
    
    with tab3:
        st.header("📋 Market Summary")
        
        # Market overview
        st.subheader("Market Overview")
        
        # Get Indian market indices
        market_indices = {
            "^NSEI": "NIFTY 50",
            "^BSESN": "SENSEX",
            "^NSEBANK": "NIFTY BANK",
            "^CNXIT": "NIFTY IT"
        }
        
        market_data = []
        for index_symbol, index_name in market_indices.items():
            try:
                index_data, index_info = get_stock_data(index_symbol, "1d")
                if index_data is not None and not index_data.empty:
                    current_value = index_data['Close'].iloc[-1]
                    previous_value = index_data['Open'].iloc[0]
                    change = current_value - previous_value
                    change_pct = (change / previous_value) * 100
                    
                    market_data.append({
                        'Index': index_name,
                        'Value': current_value,
                        'Change': change,
                        'Change %': change_pct
                    })
            except:
                continue
        
        if market_data:
            df_market = pd.DataFrame(market_data)
            
            # Display market indices
            col1, col2, col3, col4 = st.columns(4)
            for i, (_, row) in enumerate(df_market.iterrows()):
                with [col1, col2, col3, col4][i]:
                    st.metric(
                        label=row['Index'],
                        value=f"{row['Value']:.2f}",
                        delta=f"{row['Change']:.2f} ({row['Change %']:.2f}%)",
                        delta_color="normal" if row['Change'] >= 0 else "inverse"
                    )
        
        # Market sentiment
        st.subheader("Market Sentiment")
        
        if selected_stocks:
            sentiment_data = []
            for symbol in selected_stocks:
                stock_data, _ = get_stock_data(symbol, "1d")
                if stock_data is not None and not stock_data.empty:
                    current_price = stock_data['Close'].iloc[-1]
                    open_price = stock_data['Open'].iloc[0]
                    sentiment = "Bullish" if current_price > open_price else "Bearish"
                    
                    sentiment_data.append({
                        'Symbol': symbol,
                        'Sentiment': sentiment,
                        'Price Change': current_price - open_price
                    })
            
            if sentiment_data:
                df_sentiment = pd.DataFrame(sentiment_data)
                
                # Sentiment distribution
                sentiment_counts = df_sentiment['Sentiment'].value_counts()
                
                fig_sentiment = px.pie(
                    values=sentiment_counts.values,
                    names=sentiment_counts.index,
                    title="Market Sentiment Distribution",
                    color_discrete_map={'Bullish': 'green', 'Bearish': 'red'}
                )
                
                st.plotly_chart(fig_sentiment, use_container_width=True)

# Auto-refresh functionality
if auto_refresh:
    time.sleep(30)
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>📊 Real-Time Stock Market Dashboard | Data provided by Yahoo Finance</p>
        <p>Last updated: {}</p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    unsafe_allow_html=True
)
