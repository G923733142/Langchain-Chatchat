import streamlit as st

contain = st.container()

if st.session_state['messages'] == None:
    st.session_state['messages'] = []

prompt = st.chat_input("say it")
if prompt:
    st.session_state['messages'].append(prompt)


# st.write(f"{st.session_state.keys()}")
# st.write(f"{st.session_state.values()}")
# st.write(f'{st.session_state["messages"]}')

with contain:
    with st.chat_message("user"):
        if st.session_state['messages']:
            for message in st.session_state["messages"]:
                st.write(message)