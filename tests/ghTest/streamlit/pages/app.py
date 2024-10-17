import streamlit as st
from streamlit import text_area
from svgwrite.data.svgparser import number

# streamlit run app.py

number =st.slider("Pick a number", 0, 100)
size = st.select_slider("Pick a size", ["S", "M", "L"])

if st.button("Say hello"):
    st.write("Why hello there")
else:
    st.write("Goodbye")
# 切换会导致页面刷新 ,复选，单选，激活 都会，
checkbox = st.checkbox("yes")
st.write("checkbox: ", checkbox)

activated = st.toggle("Activate")
st.write("activate:" , activated)

radio = st.radio("radio", ['cats', 'dogs'])
st.write("radio", radio)

selected = st.selectbox("selectbox", ['cats', 'cats', 'cats',  'dogs'])
st.write("selected: ", selected)

multiselect = st.multiselect("multiselect", ['cats', 'cats', 'cats',  'dogs'])
st.write(f"multiselect: {multiselect}" )
st.write("multiselect: " ,multiselect )

name = st.text_input("Enter your name")
st.write("Hello ", name)
st.session_state['username'] = name

choice = st.number_input("Enter a number", 0, 10)

text_area = st.text_area("Enter your text")

date = st.date_input("Enter a date")

time = st.time_input("Enter a time")

data = st.file_uploader("Choose a file")

st.sidebar.write("this is a sidebar")
st.sidebar.button("this is a sidebar button")

col1, col2, col3 = st.columns(3)

col1.write("this is a col1")
col2.write("this is a col2")
col3.button("this is a col3")




tab1, tab2 = st.tabs(["tab1", "tab2"])
tab1.write("this is a tab1")
tab2.write("this is a tab2")

# with st.expender("open to see more"):
#     st.write("i am more")


if st.session_state.get('name', False):
    st.write("session name is ", st.session_state['name'])
else:
    st.write("session name is blank")