import streamlit as st
import requests

st.set_page_config(page_title="DocQuery RAG", layout="wide")

st.title("📄 DocQuery RAG: Ask Questions From Your Documents")
st.write("Upload your documents and get answers powered by Gemini and Pinecone.")

# API endpoint
API_URL = "http://backend:8000"

with st.sidebar:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload your Text or PDF files",
        accept_multiple_files=True,
        type=['pdf', 'txt']
    )

    if st.button("Process Documents"):
        if uploaded_files:
            files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
            
            with st.spinner("Processing documents... This may take a moment."):
                try:
                    response = requests.post(f"{API_URL}/upload-documents/", files=files)
                    if response.status_code == 201:
                        st.success("Documents processed and indexed successfully!")
                    else:
                        st.error(f"Error: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection error: {e}")
        else:
            st.warning("Please upload at least one document.")

st.header("Ask a Question")
user_question = st.text_input("Enter your question here:")

if st.button("Get Answer"):
    if user_question:
        with st.spinner("Searching for an answer..."):
            try:
                payload = {"query": user_question}
                response = requests.post(f"{API_URL}/query/", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    st.subheader("Answer:")
                    st.write(data["answer"])
                    
                    with st.expander("Show Retrieved Context"):
                        for i, context_chunk in enumerate(data["context"]):
                            st.write(f"**Chunk {i+1}:**")
                            st.write(context_chunk)
                else:
                    st.error(f"Error fetching answer: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {e}")
    else:
        st.warning("Please enter a question.")
