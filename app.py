import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
import time
from datetime import datetime, timedelta
import yfinance as yf

# Page configuration
st.set_page_config(
    page_title="Real-Time Stock Market Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .positive-change {
        color: #00ff00;
        font-weight: bold;
    }
    .negative-change {
        color: #ff0000;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📈 Real-Time Stock Market Dashboard</h1>', unsafe_allow_html=True)

# Sidebar for stock selection
st.sidebar.header("📊 Stock Selection")
st.sidebar.markdown("---")

# Popular stocks list
popular_stocks = {
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
    "WAAENERGIES.NS": "Waaree Energies Ltd. (India)",
    "CRESTCHM.NS": "Crestchem Ltd. (India)"
}

# Stock selection
selected_stocks = st.sidebar.multiselect(
    "Select stocks to track:",
    options=list(popular_stocks.keys()),
    default=["AAPL", "GOOGL", "MSFT"],
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

# Function to get stock data with improved error handling
@st.cache_data(ttl=60)
def get_stock_data(symbol, period="1mo"):
    """Fetch stock data using yfinance with retry logic"""
    import time
    
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            # Get proper symbol with exchange suffix
            proper_symbol = get_stock_symbol(symbol)
            stock = yf.Ticker(proper_symbol)
            
            # Add a small delay to avoid rate limiting
            time.sleep(0.5)
            
            # Fetch historical data with longer timeout for Indian stocks
            if '.NS' in symbol or '.BO' in symbol:
                hist = stock.history(period=period, progress=False, timeout=30)
            else:
                hist = stock.history(period=period, progress=False)
            
            # Add delay before fetching info
            time.sleep(0.5)
            
            # Fetch stock info
            info = stock.info
            
            # Validate data
            if hist is None or hist.empty:
                st.warning(f"No data available for {symbol}. Please check the symbol.")
                return None, None
            
            return hist, info
            
        except Exception as e:
            if attempt < max_retries - 1:
                st.warning(f"Attempt {attempt + 1} failed for {symbol}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                st.error(f"Failed to fetch data for {symbol} after {max_retries} attempts: {str(e)}")
                return None, None
    
    return None, None

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
    
    # Update layout
    fig.update_layout(
        title=f"{symbol} - {stock_info.get('longName', symbol)}",
        xaxis_rangeslider_visible=False,
        height=800,
        showlegend=True,
        template="plotly_white"
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
        high_52w = stock_info.get('fiftyTwoWeekHigh', 0)
        st.metric(
            label="52W High",
            value=f"${high_52w:.2f}",
            delta=None
        )
    
    with col4:
        low_52w = stock_info.get('fiftyTwoWeekLow', 0)
        st.metric(
            label="52W Low",
            value=f"${low_52w:.2f}",
            delta=None
        )

# Main dashboard
if selected_stocks:
    # Show loading status
    with st.spinner("🔄 Fetching real-time stock data..."):
        pass
    
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
            
            # Display portfolio table
            st.dataframe(
                df_portfolio.style.format({
                    'Price': '${:.2f}',
                    'Change': '${:.2f}',
                    'Change %': '{:.2f}%',
                    'Volume': '{:,.0f}'
                }).background_gradient(subset=['Change %'], cmap='RdYlGn'),
                use_container_width=True
            )
            
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
                
                fig_performance.update_layout(
                    title="Portfolio Performance Comparison (Normalized to 100)",
                    xaxis_title="Date",
                    yaxis_title="Performance (%)",
                    template="plotly_white"
                )
                
                st.plotly_chart(fig_performance, use_container_width=True)
    
    with tab3:
        st.header("📋 Market Summary")
        
        # Market overview
        st.subheader("Market Overview")
        
        # Get market indices
        market_indices = {
            "^GSPC": "S&P 500",
            "^DJI": "Dow Jones",
            "^IXIC": "NASDAQ",
            "^VIX": "VIX Volatility"
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
