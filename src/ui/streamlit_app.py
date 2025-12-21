import streamlit as st
import requests

# Configuration
API_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(page_title="EIKA Knowledge Assistant", page_icon="🤖")

st.title("🤖 EIKA Knowledge Assistant")

# 1. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Display Chat History on every rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Handle User Input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 4. Call Backend API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                payload = {"text": prompt, "limit": 3}
                response = requests.post(f"{API_URL}/query/chat", json=payload)
                response.raise_for_status()
                data = response.json()
                
                ai_answer = data.get("ai_response", "No response received.")
                sources = data.get("source_documents", [])
                
                # Format the answer
                full_response = ai_answer
                
                # Append Sources if available
                if sources:
                    full_response += "\n\n**Sources:**"
                    for idx, source in enumerate(sources, 1):
                        page = source['metadata'].get('page', 'Unknown')
                        # Clean up newlines for display
                        clean_content = source['content'][:100].replace("\n", " ")
                        full_response += f"\n{idx}. Page {page}: _{clean_content}..._"

                st.markdown(full_response)
                
                # Add assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                error_msg = f"❌ Error connecting to backend: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})