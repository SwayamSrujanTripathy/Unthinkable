import streamlit as st
import requests
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    layout="wide",
    page_title="Mnemo",
    page_icon="🤖"
)

# --- CUSTOM CSS FOR ENHANCED FUTURISTIC UI ---
st.markdown("""
<style>
    @keyframes gradient-animation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes float {
        0% { transform: translateY(0px); text-shadow: 0 5px 15px rgba(0,0,0,0.6); }
        50% { transform: translateY(-15px); text-shadow: 0 25px 30px rgba(0,0,0,0.5); }
        100% { transform: translateY(0px); text-shadow: 0 5px 15px rgba(0,0,0,0.6); }
    }

    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(94, 234, 212, 0.7); }
        70% { transform: scale(1.05); box-shadow: 0 0 0 15px rgba(94, 234, 212, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(94, 234, 212, 0); }
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Cursor trail effect */
    .cursor-trail {
        position: fixed;
        width: 12px;
        height: 12px;
        background: radial-gradient(circle, rgba(94, 234, 212, 0.8) 20%, rgba(94, 234, 212, 0) 80%);
        border-radius: 50%;
        pointer-events: none;
        z-index: 9999;
        transition: transform 0.1s ease-out, opacity 0.3s ease-out;
        opacity: 0;
    }
    .cursor-trail.active {
        opacity: 1;
        animation: pulse 0.6s ease infinite;
    }

    /* Main app background with animated gradient */
    .stApp {
        background: linear-gradient(225deg, #0D1117, #1F2937, #374151, #4B5EAA);
        background-size: 600% 600%;
        color: #E5E7EB;
        animation: gradient-animation 15s ease infinite;
    }

    /* Title styling with enhanced gradient and floating effect */
    h1 {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 3rem;
        text-align: center;
        background: linear-gradient(90deg, #5EEAD4, #A78BFA, #F472B6, #5EEAD4);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-animation 5s ease infinite, float 5s ease-in-out infinite;
        margin-bottom: 1rem;
    }

    /* Subtitle styling */
    p {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        text-align: center;
        color: #D1D5DB;
        animation: fadeIn 1.5s ease-out;
    }

    /* Slimmer sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #161B22, #1F2937);
        max-width: 350px;
        padding: 1rem;
        box-shadow: 2px 0 10px rgba(0,0,0,0.5);
        animation: fadeIn 0.8s ease-out;
    }
    /* Button styling with neon glow */
    .stButton>button {
        border-radius: 15px;
        border: 2px solid #B6E3E1;
        background: linear-gradient(45deg, #1F2937, #374151);
        color: #19333B;
        font-family: 'Inter', sans-serif;
        font-weight: bold;
        padding: 12px 24px;
        transition: all 0.3s ease-in-out;
        position: relative;
        overflow:hidden;
    }
    .stButton>button:hover {
        background: #19333B;
        color: #0D1117;
        box-shadow: 0 0 25px rgba(94, 234, 212, 0.7);
        transform: translateY(-3px);
    }
    /*.stButton>button::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 300%;
        height: 300%;
        background: rgba(255, 255, 255, 0.1);
        transform: translate(-50%, -50%) rotate(45deg);
        transition: all 0.5s ease;
        opacity: 0;
    }
    .stButton>button:hover::after {
        opacity: 1;
        width: 0;
        height:0;
    }/*



    /* Answer box styling with hover animation */
    .answer-box {
        background: #1F2937;
        border-left: 8px solid #A78BFA;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        margin-top: 1.5rem;
        font-family: 'Inter', sans-serif;
        font-size: 1.15rem;
        color: #E5E7EB;
        transition: all 0.4s ease-in-out;
        animation: fadeIn 1s ease-out;
    }
    .answer-box:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.5);
        border-left-color: #5EEAD4;
    }

    /* Text input styling with subtle glow */
    .stTextInput>div>div>input {
        background: #1F2937;
        color: #E5E7EB;
        border-radius: 12px;
        border: 1px solid #5EEAD4;
        padding: 0.75rem;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    .stTextInput>div>div>input:focus {
        box-shadow: 0 0 15px rgba(94, 234, 212, 0.5);
        border-color: #A78BFA;
    }

    /* File uploader styling */
    .stFileUploader {
        background: #161B22;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #5EEAD4;
        animation: fadeIn 1s ease-out;
    }

    /* Spinner and toast styling */
    .stSpinner>div>span {
        color: #5EEAD4;
    }
    .stToast {
        background: #1F2937;
        border: 1px solid #A78BFA;
        color: #E5E7EB;
        border-radius: 10px;
    }
</style>
<script>
    // Cursor trail effect
    document.addEventListener('DOMContentLoaded', () => {
        const trail = document.createElement('div');
        trail.className = 'cursor-trail';
        document.body.appendChild(trail);

        document.addEventListener('mousemove', (e) => {
            trail.style.left = `${e.clientX}px`;
            trail.style.top = `${e.clientY}px`;
            trail.classList.add('active');
        });

        document.addEventListener('mouseout', () => {
            trail.classList.remove('active');
        });
    });
</script>
""", unsafe_allow_html=True)

# --- BACKEND URL CONFIGURATION ---
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# --- UI LAYOUT ---
st.title("🤖 Mnemo: Your Personal Document Assistant")
st.markdown("<p style='text-align: center; color: #9CA3AF;'>Upload your documents, ask complex questions, and get intelligent answers instantly.</p>", unsafe_allow_html=True)

# --- SIDEBAR FOR DOCUMENT UPLOADS ---
with st.sidebar:
    st.image(
        "Mnemo.jpg",
        use_container_width=True
    )
    st.header("📤 Upload Your Knowledge Base")
    uploaded_files = st.file_uploader(
        "Choose PDF or TXT files",
        accept_multiple_files=True,
        type=['pdf', 'txt'],
        help="You can upload multiple documents at once."
    )

    if st.button("🚀 Process Documents") and uploaded_files:
        with st.spinner("Analyzing documents... This may take a moment."):
            files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
            try:
                response = requests.post(f"{BACKEND_URL}/upload-documents/", files=files)
                if response.status_code == 200:
                    st.success("✅ Documents processed successfully!")
                    st.toast("Your new knowledge base is ready.")
                else:
                    st.error(f"Error: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Connection Error")
                st.info("Could not connect to the backend. Please ensure it's running.")

# --- MAIN CONTENT AREA FOR Q&A ---
st.header("💡 Ask a Question")
user_input = st.text_input(
    "Enter your question based on the uploaded documents:",
    placeholder="e.g., What were the key findings in the Q3 report?",
    label_visibility="collapsed"
)

if user_input:
    with st.spinner("🧠 Thinking..."):
        try:
            payload = {"text": user_input}
            response = requests.post(f"{BACKEND_URL}/query/", json=payload)

            if response.status_code == 200:
                answer = response.json().get("answer", "No answer could be generated from the documents.")
                st.markdown("### Answer")
                st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)
            else:
                st.error(f"Failed to get an answer: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Connection Error")
            st.info("Could not connect to the backend. Please ensure it's running.")

else:
    st.info("Please upload and process documents in the sidebar to begin asking questions.")