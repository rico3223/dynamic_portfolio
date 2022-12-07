import streamlit as st

import numpy as np
import pandas as pd

import dynamic_portfolio.preprocess as prep
import dynamic_portfolio.utils as utils

st.title("""
            Building winning financial portfolios
            """)




#col1, col2, col3 = st.columns(3)
#with col1:

choice = st.selectbox("Choose a ticker (⬇💬👇ℹ️ ...)", utils.return_tickers())

df = prep.ready_to_train_df(choice)
df2 = df[['gdp_return','return']]

st.line_chart(df2)

#ticker = st.text_input("Choose a ticker (⬇💬👇ℹ️ ...)", value="⬇")
#with col2:
#    ticker_dx = st.slider(
#        "Horizontal offset", min_value=-30, max_value=30, step=1, value=0
#    )
#with col3:
#    ticker_dy = st.slider(
#        "Vertical offset", min_value=-30, max_value=30, step=1, value=-10
#    )

st.dataframe(df)

line_count = st.slider('Select a line count', 1, 10, 3)

head_df = df.head(line_count)

head_df
