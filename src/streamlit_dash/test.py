import streamlit as st
import pandas as pd
import numpy as np

st.write("# Test: Enkel graf i Streamlit")

data = pd.DataFrame(np.random.randn(10, 1), columns=["value"])
st.line_chart(data)

import sys
import os
sys.path.append('C:/Users/Brukare/Desktop/github/data_enginer_trion/src')