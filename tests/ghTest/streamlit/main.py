import streamlit as st
import numpy as np
import pandas as pd
import time
import os

# streamlit run app.py

# st.page_link("pages/app.py", label="Home" )
# st.page_link("pages/profile.py", label="My profile"  )

st.write("#hello \n **world**")
st.write("# hello")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"]
)
st.write(chart_data)

def my_generator():
    for i in range(10):
        yield f'{i}'
        time.sleep(0.5)
# st.write(my_generator)

st.markdown("# H1")
"## H2"

st.title("this is title")

st.header("this is header")

st.code('a == 1234')

st.divider()

st.json({ "aaa": "aaa"})

text_content = """ this is a text """
st.download_button(" download some text", text_content)

st.link_button("clike to baidu", "http://www.baidu.com")

# 切换会导致页面刷新
selected = st.checkbox("yes")

activated = st.toggle("Activate")
st.write("activate:" , activated)


# path = os.path.relpath("pages/app.py")
# st.page_link(str(path), label="Home", icon="🏠")


