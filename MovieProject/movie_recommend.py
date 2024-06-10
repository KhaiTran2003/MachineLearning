import streamlit as st

st.title('Movies Recommend System')
option = st.selectbox(
    'How would you like to be contacted?',
    ('Email','Phone','Mobile Phone')
)