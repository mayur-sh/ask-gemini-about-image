import google.generativeai as genai
import google.ai.generativelanguage as glm
import streamlit as st


genai.configure(api_key=st.secrets.get('gemini-api-key'))

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 10000,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]
model = genai.GenerativeModel('gemini-pro-vision', safety_settings, generation_config)


# Sidebar
with st.sidebar:
    st.markdown("""
    <style>
        .icon {
            transition: transform 0.3s ease-in-out;
        }
        .icon:hover {
            transform: scale(1.05);
        }
        .side-bar {
            display: flex;
            justify-content: center;
        }
    </style>

    <div class="side-bar">
        <a href="https://www.linkedin.com/in/mayur-sh">
        <img src="https://cliply.co/wp-content/uploads/2021/02/372102050_LINKEDIN_ICON_TRANSPARENT_1080.gif" alt="Linkedin" width="100px" class="icon">
        </a>
    </div>
""", unsafe_allow_html=True)



# Header and Line
st.markdown("""
    <h2 style="text-align:center;"> Get answers about your image! </h2>
""", unsafe_allow_html=True)
st.header("", divider='rainbow')

st.markdown("""
    <p style="text-align:right;">~ By Snehal Kapadi</p>
""", unsafe_allow_html=True)


# File Uploader
img = st.file_uploader('',type=["jpg", "png", "jpeg"])

prompt = st.text_input("Ask your question:", value="Give the detailed explaination about the image and the things in it.")

if img:
    if st.button("Get the answer!"):
            # Snow Effect
        st.snow()

        # Spinner bar
        with st.spinner("Getting the results from GEMINI✨"):

            # Getting response from Gemini API
            response = model.generate_content(
                glm.Content(
                    parts = [
                        glm.Part(text=prompt),
                        glm.Part(
                            inline_data=glm.Blob(
                                mime_type=img.type,
                                data=img.read()
                            )
                        ),
                    ],
                ),
                stream=True)

            response.resolve()


        st.write(response.text)

