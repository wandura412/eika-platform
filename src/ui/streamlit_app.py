import streamlit as st
import requests

# Configuration
API_BASE_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(page_title="EIKA Knowledge Assistant", page_icon="🤖", layout="wide")

st.title("EIKA Knowledge Assistant")

# --- SIDEBAR: CONFIGURATION & UPLOAD ---
with st.sidebar:
    st.header("🗂️ Document Manager")
    
    # 1. Reset Database Button
    if st.button("🗑️ Reset / Clear Database", type="primary"):
        try:
            response = requests.delete(f"{API_BASE_URL}/documents/reset")
            if response.status_code == 200:
                st.toast("Knowledge base cleared successfully!", icon="🗑️")
            else:
                st.error("Failed to clear database.")
        except Exception as e:
            st.error(f"Connection Error: {e}")

    st.markdown("---")

    # 2. File Uploader
    uploaded_file = st.file_uploader("Upload a PDF Document", type=["pdf"])
    
    # 3. Upload Button Logic
    if uploaded_file is not None:
        if st.button("📤 Ingest Document"):
            with st.spinner("Processing document... (This may take a moment)"):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                    response = requests.post(f"{API_BASE_URL}/documents/ingest", files=files)
                    
                    if response.status_code == 200:
                        st.toast(f"Successfully ingested: {uploaded_file.name}", icon="📄")
                    else:
                        st.error(f"Upload failed: {response.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")

# --- MAIN CHAT INTERFACE ---

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle User Input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call Backend API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                payload = {"text": prompt, "limit": 3}
                response = requests.post(f"{API_BASE_URL}/query/chat", json=payload)
                response.raise_for_status()
                data = response.json()
                
                ai_answer = data.get("ai_response", "No response received.")
                sources = data.get("source_documents", [])
                
                full_response = ai_answer
                
                # Append Sources
                if sources:
                    full_response += "\n\n**Sources:**"
                    for idx, source in enumerate(sources, 1):
                        page = source['metadata'].get('page', 'Unknown')
                        clean_content = source['content'][:150].replace("\n", " ")
                        full_response += f"\n{idx}. Page {page}: _{clean_content}..._"

                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                error_msg = f"Error connecting to backend: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})