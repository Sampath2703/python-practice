import streamlit as st
st.title("Student Login")

login,signup = st.tabs(
    ["Login", "Signup"]

)


with login:
    st.header("Login")

    with st.form("Loing_Form"):

        st.text_input("Email")
        st.text_input("Password", type="password")
        st.form_submit_button("Login")

with signup:
    st.header("Signup")
    with st.form("signup_Form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password",type="password")
        btn=st.form_submit_button("SignUp")




