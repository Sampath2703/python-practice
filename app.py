from click import option
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
    opt = st.sidebar.selectbox(
        "Select an Option",
        ["Upload File", "View Files", "Logout"]
    )
    st.header("Dashboard")
    if opt == "Upload File":
        st.subheader("Upload Your Media Files")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["jpg", "jpeg", "png", "mp4", "mp3", "pdf"]
        )

        if uploaded_file is not None:
            st.write(uploaded_file.name)

            st.write(uploaded_file.type)

            if "image" in uploaded_file.type:

                st.image(uploaded_file)

            elif "video" in uploaded_file.type:

                st.video(uploaded_file)

            elif "audio" in uploaded_file.type:

                st.audio(uploaded_file)

            if st.button("Upload File to Cloudinary"):

                upload_dict_obj = cloudinary.uploader.upload(
                    uploaded_file,
                    resource_type="auto"
                )

                url = upload_dict_obj["secure_url"]

                file_name = uploaded_file.name

                file_type = uploaded_file.type

                query = """
                INSERT INTO files(file_name,file_url,file_type)
                VALUES(%s,%s,%s)
                """

                values = (file_name, url, file_type)

                cursor.execute(query, values)

                conn.commit()

                st.success("File Uploaded Successfully")

    elif opt == "View Files":

        st.subheader("All Uploaded Files")

        cursor.execute("SELECT * FROM files")

        data = cursor.fetchall()

        if len(data) == 0:

            st.warning("No Records Found")

        else:

            for row in data:
                file_name = row["file_name"]
                file_url = row["file_url"]
                file_type = row["file_type"]
                
                st.write("File Name:", file_name)

                if "image" in file_type:

                    st.image(file_url)
                    st.write("File Type:", file_type)

                elif "video" in file_type:

                    st.video(file_url)
                    st.write("File Type:", file_type)

                elif "audio" in file_type:

                    st.audio(file_url)
                    st.write("File Type:", file_type)

                else:

                    st.link_button("Open File", file_url)
            
    

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



