
import streamlit as st
import requests
import os

# Backend API configuration
API_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api/v1")

st.set_page_config(
    page_title="Blog Generation Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🤖 Blog Generation Agent")
st.markdown("Generate high-quality blog posts using autonomous AI agents.")

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    
    style = st.selectbox(
        "Writing Style",
        ["professional", "casual", "technical", "humorous"],
        index=0,
        help="Select the tone and style of the blog post."
    )
    
    target_language = st.selectbox(
        "Target Language (Optional)",
        ["English", "Spanish", "French", "German", "Chinese"],
        index=0,
        help="Select a language to translate the blog post into."
    )
    # Streamlit treats the first option as selected, so we handle "English" as None or default in logic if needed
    # But the API might expect None for no translation. 
    # Let's check api_models.py. If "English" is default, maybe we pass None if it matches source.
    # For now, let's keep it simple.

    st.divider()
    st.info("Check the backend health:")
    if st.button("Check Health"):
        try:
            response = requests.get(f"{API_URL}/health")
            if response.status_code == 200:
                data = response.json()
                st.success(f"System Operational v{data.get('version')}")
            else:
                st.error("Backend unhealthy")
        except Exception as e:
            st.error(f"Connection failed: {e}")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Input")
    
    topic = st.text_area(
        "Blog Topic",
        height=100,
        placeholder="Enter the main topic or title e.g., 'The Future of AI Agents'"
    )
    
    transcript = st.text_area(
        "Source Material / Transcript (Optional)",
        height=200,
        placeholder="Paste any background context, transcript, or notes here..."
    )
    
    generate_btn = st.button("🚀 Generate Blog Post", type="primary", use_container_width=True)

with col2:
    st.subheader("Output")
    
    if generate_btn:
        if not topic:
            st.warning("Please enter a topic first.")
        else:
            with st.spinner("Agents are working... (Planning, Writing, Translating)"):
                try:
                    payload = {
                        "topic": topic,
                        "transcript": transcript if transcript else None,
                        "style": style,
                        "target_language": target_language if target_language != "English" else None
                    }
                    
                    response = requests.post(f"{API_URL}/generate", json=payload)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.success(f"Generated in {result['generation_time_seconds']}s")
                        
                        st.markdown(f"### {result['title']}")
                        st.markdown(result['content'])
                        
                        with st.expander("Metadata"):
                            st.json({
                                "Word Count": result['word_count'],
                                "Translated": result['was_translated'],
                                "Brainstormed Titles": result['brainstormed_titles']
                            })
                    else:
                        st.error(f"Error: {response.status_code}")
                        st.json(response.json())
                        
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
