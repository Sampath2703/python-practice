import cloudinary
import cloudinary.uploader
import streamlit as st
from db_c import cursor, conn

st.title("Media Platform")


cloudinary.config(
    cloud_name = st.secrets["cloud_name"],
    api_key = st.secrets["api_key"],
    api_secret = st.secrets["api_secret"]
)

if "user" not in st.session_state:
    st.session_state.user = None

def dashboard():
    st.sidebar.success("Welcome to Dashboard")
    opt = st.sidebar.selectbox("Select an Option", ["Upload File", "View Files", "Logout"])
    st.header("dashboard")

    if opt == "Upload File":
        st.subheader("Upload Your Media Files")
        uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png", "mp4", "mp3","pdf"])
        if uploaded_file:
            st.write(uploaded_file.name)
            st.write(uploaded_file.type )

        if "image" in uploaded_file.type:
            st.image(uploaded_file)
        elif "video" in uploaded_file.type:
            st.video(uploaded_file)
        elif "audio" in uploaded_file.type:
            st.audio(uploaded_file)

        if st.button("Upload file to cloudinary"):
            upload_dict_obj = cloudinary.uploader.upload(uploaded_file, resourse_type="auto")
            url = upload_dict_obj["secure_url"]
            st.write(url)
            st.write("File Uploaded to cloudinary successfully")


    elif opt == "Logout":
        st.session_state.user = None
        st.success("Logged out successfully")
        st.rerun()
    

def login_function():
    st.header("Login")

    with st.form("Loing_Form"):

        email =st.text_input("Email")
        password = st.text_input("Password", type="password")
        btn = st.form_submit_button("Login")
        if btn:
            query = "SELECT * FROM users WHERE email = %s AND password = %s"
            values = (email, password)
            cursor.execute(query, values)
            user = cursor.fetchone()
            st.session_state.user = user
            st.write("Login successful")
            st.rerun()
        

def signup_function():
    st.header("Signup")
    with st.form("signup_Form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password",type="password")
        btn=st.form_submit_button("SignUp")

        if btn:
            query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            values = (name, email, password)
            cursor.execute(query, values)
            conn.commit()
            st.write("User added successfully")

if st.session_state.user == None:
    login,signup = st.tabs(
    ["Login", "Signup"]
    )

    with signup:
        signup_function()

    with login:
        login_function()

else:
    dashboard()



