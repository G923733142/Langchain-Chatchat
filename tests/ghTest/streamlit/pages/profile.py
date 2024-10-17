import pandas as pd
import streamlit as st
import numpy as np
# streamlit run app.py

c = st.container()
st.write("hello profile")
c.write("this is a c1")
c.write("this is a c2")

if st.button("Say hello"):
    st.write("Why hello there")
else:
    st.write("Goodbye")


name = st.text_input("Name")
if name:
    st.write("Hello ", name)
prompt = st.chat_input("Say something")
if prompt:
    st.write("send ", prompt)

with st.chat_message("user"):
    st.write("Hello, ")
    st.line_chart(np.random.randn(30, 3))

with st.chat_message("ai"):
    st.write("Hello, i am ai")

with st.echo():
    st.write("this is code")

st.help(st.write)
st.help(pd.DataFrame)

st.session_state['name'] = 'gh'

if st.session_state.get('username', False):
    st.write(f"get from session : {st.session_state['username']}")