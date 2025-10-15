import streamlit as st
import requests
import os

# Updated to use localhost for local development
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(layout="wide", page_title="Document RAG System")

st.title("📄 Retrieval-Augmented Generation (RAG) System")
st.markdown("Upload your documents (PDF or TXT) and ask questions about them.")

with st.sidebar:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose PDF or TXT files",
        accept_multiple_files=True,
        type=['pdf', 'txt']
    )

    if st.button("Process Documents") and uploaded_files:
        with st.spinner("Processing documents... This may take a moment."):
            files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
            try:
                response = requests.post(f"{BACKEND_URL}/upload-documents/", files=files)
                if response.status_code == 200:
                    st.success("Documents processed and indexed successfully!")
                else:
                    st.error(f"Error processing documents: {response.text}")
            except requests.exceptions.ConnectionError as e:
                st.error(f"Connection error: {e}")
                st.info("Please ensure the backend service is running and accessible.")

st.header("Ask a Question")
user_input = st.text_input("Enter your question based on the uploaded documents:")

if user_input:
    with st.spinner("Searching for an answer..."):
        try:
            # FIX: The JSON payload key must match the Pydantic model in the backend.
            # Changed 'query' to 'text'.
            payload = {"text": user_input}
            response = requests.post(f"{BACKEND_URL}/query/", json=payload)

            if response.status_code == 200:
                answer = response.json().get("answer")
                st.subheader("Answer:")
                st.write(answer)
            else:
                st.error(f"Failed to get an answer: {response.text}")
        except requests.exceptions.ConnectionError as e:
            st.error(f"Connection error: {e}")
            st.info("Please ensure the backend service is running and accessible.")

