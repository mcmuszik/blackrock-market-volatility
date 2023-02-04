import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.header('BlackRock Market Volatility')
st.subheader('created by Marc Muszik and John Black')

data = dict(
    character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
    parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
    value=[10, 14, 12, 10, 2, 6, 6, 4, 4])

fig = px.sunburst(
    data,
    names='character',
    parents='parent',
    values='value',
)

st.plotly_chart(fig, theme=None, use_container_width=True)