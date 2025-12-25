

import streamlit as st


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
		# st.write('**Face Value (Screener.in):**', screener_data['face_value'])
		if screener_data['shareholding_pattern']:
			st.write('**Shareholding Pattern (Screener.in):**')
			# Display as a static table (not scrollable)
			import pandas as pd
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
		else:
			st.write('Shareholding pattern not found on Screener.in')
