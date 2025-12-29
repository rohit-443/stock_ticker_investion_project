import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re

# Pastel gradient background and left alignment for the entire Streamlit page
st.markdown(
    """
    <style>
    body, .main, .block-container {
        background: linear-gradient(135deg, #ffe5b4 0%, #fff9c4 100%);
        min-height: 100vh;
        margin: 0;
        padding: 0;
        text-align: left !important;
        align-items: flex-start !important;
        justify-content: flex-start !important;
    }
    .block-container {
        margin-left: 0 !important;
        padding-left: 2rem !important;
        padding-right: 0 !important;
        max-width: 100vw !important;
        width: 100vw !important;
    }
    .stTextInput, .stMarkdown, .stDataFrame, .stTable, .stSubheader, .stError, .stAlert, .stText, .stWrite, .stHeading, .stTitle {
        text-align: left !important;
        align-items: flex-start !important;
        justify-content: flex-start !important;
        background: rgba(255,255,255,0.7);
        border-radius: 8px;
        padding: 8px 12px;
        box-shadow: 0 2px 8px rgba(160,160,160,0.05);
    }
    .shareholding-table td, .shareholding-table th {
        text-align: left !important;
        padding-left: 8px !important;
        background: rgba(255,255,255,0.8);
    }
    .shareholding-table {
        width: 100% !important;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(160,160,160,0.08);
    }
    </style>
    """,
    unsafe_allow_html=True
)

from src.data_providers import get_ticker_data, get_screener_data

st.title('Stock Ticker Investigation')

# Text input for ticker symbol
ticker_symbol = st.text_input('Enter Ticker Symbol (e.g., RELIANCE.NS):', 'RELIANCE.NS')

if ticker_symbol:
    data, error = get_ticker_data(ticker_symbol)
    screener_data, screener_error = get_screener_data(ticker_symbol)

    if error:
        st.error(f"Error fetching data: {error}")
    elif data:
        st.subheader(f'Results for {ticker_symbol}')
        # Display metrics in 3 columns, 3 rows (3-3-2)
        col1, col2, col3 = st.columns(3)
        market_cap_crores = None
        if data['market_cap'] is not None:
            try:
                market_cap_crores = float(data['market_cap']) / 10000000
            except Exception:
                market_cap_crores = data['market_cap']
        col1.markdown(f"**Market Cap:**<br>{market_cap_crores:.3f} Cr" if market_cap_crores is not None else f"**Market Cap:**<br>N/A", unsafe_allow_html=True)
        col2.markdown(f"**52 Week High:**<br>{data['week_52_high']}", unsafe_allow_html=True)
        col3.markdown(f"**52 Week Low:**<br>{data['week_52_low']}", unsafe_allow_html=True)

        col1.markdown(f"**All Time High:**<br>{data['all_time_high']}", unsafe_allow_html=True)
        col2.markdown(f"**All Time Low:**<br>{data['all_time_low']}", unsafe_allow_html=True)
        col3.markdown(f"**Script P/E:**<br>{data['pe_ratio']}", unsafe_allow_html=True)

        col1.markdown(f"**Sector P/E:**<br>{data['sector_pe']}", unsafe_allow_html=True)
        col2.markdown(f"**Face Value (Screener.in):**<br>{screener_data['face_value'] if screener_data else ''}", unsafe_allow_html=True)

    # Show Screener.in data
    if screener_error:
        st.error(f"Screener.in error: {screener_error}")
    elif screener_data:
        if screener_data['shareholding_pattern']:
            st.write('**Shareholding Pattern (Screener.in):**')
            # Display as a static table (not scrollable)
            df = pd.DataFrame(screener_data['shareholding_pattern'][1:], columns=screener_data['shareholding_pattern'][0] if screener_data['shareholding_pattern'] else None)
            
            # Custom CSS for left-align and full width
            st.markdown(
                """
                <style>
                .shareholding-table td, .shareholding-table th {
                    text-align: left !important;
                    padding-left: 8px !important;
                }
                .shareholding-table {
                    width: 100% !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            # Render as HTML for full width and left alignment
            st.markdown(df.to_html(classes='shareholding-table', index=False, border=0, justify='left'), unsafe_allow_html=True)

            # ===== COMBINED GROUPED BAR CHART =====
            if len(df.columns) > 1:
                timeline_cols = df.columns[1:]
                cats = [cat for cat in df.iloc[:, 0].tolist() if 'no. of shareholder' not in cat.lower()]
                
                # Extract years from timeline columns
                year_map = {}
                for col in timeline_cols:
                    match = re.search(r'(\d{4})', col)
                    if match:
                        year = match.group(1)
                        year_map.setdefault(year, []).append(col)
                years = sorted(year_map.keys(), reverse=True)  # Most recent first
                
                # Define colors for each category
                colors = [
                    'rgba(255, 99, 71, 0.8)',    # Tomato
                    'rgba(54, 162, 235, 0.8)',   # Blue
                    'rgba(75, 192, 75, 0.8)',    # Green
                    'rgba(255, 206, 86, 0.8)',   # Yellow
                    'rgba(153, 102, 255, 0.8)',  # Purple
                ]
                
                # Create SINGLE figure with all categories
                fig = go.Figure()
                
                # Add a trace for each category
                for cat_idx, cat in enumerate(cats):
                    idx = df[df.iloc[:, 0] == cat].index[0]
                    
                    # For each year, average the values for that year
                    y_vals = []
                    for year in years:
                        vals = []
                        for col in year_map[year]:
                            try:
                                v = float(str(df.loc[idx, col]).replace('%','').replace(',',''))
                                vals.append(v)
                            except Exception:
                                pass
                        y_vals.append(sum(vals)/len(vals) if vals else None)
                    
                    # Add trace for this category
                    fig.add_trace(go.Bar(
                        x=years,
                        y=y_vals,
                        name=cat,  # Legend name
                        marker_color=colors[cat_idx % len(colors)],
                        text=[f"<b>{v:.1f}%</b>" if v is not None else '' for v in y_vals],
                        textposition='inside',
                    ))
                
                # Update layout for grouped bars
                fig.update_layout(
                    barmode='group',  # Group bars by year
                    title_text='Shareholding Pattern Comparison',
                    xaxis=dict(title='Year', tickfont=dict(size=12)),
                    yaxis=dict(title='Share (%)', range=[0, 100], tickvals=[0, 25, 50, 75, 100], tickfont=dict(size=11)),
                    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                    bargap=0.15,
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=500,
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                fig.update_traces(textfont_size=11)
                
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('Shareholding pattern not found on Screener.in')
