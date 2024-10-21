# Modules
import streamlit as st
from scrape import Scrape
from llm import LLM
# ===================================================================== #

# streamlit UI
st.title("AI Web Scraper")
url = st.text_input(label="", placeholder="Website URL...", autocomplete="off")

# Extracting content
if (st.button("Extract page content")) and (url):
    st.write("Extracting data...")
    
    # extracting website contnet
    scraper = Scrape(url)
    html = scraper.extract_html()
    content = scraper.extract_content(html)
    
    # store the DOM content in a session state
    st.session_state["content"] = content

    # display the content in a textarea
    with st.expander("View DOM content"):
        st.text_area(label="", value=content, height=300)

# Scraping with LLM
if ("content" in st.session_state):
    description = st.text_area(label="", placeholder="Describe what do you want to scrape...")

    if (st.button("AI Scrape")) and (description):
        content = st.session_state["content"]

        model = LLM(content, description)
        response_stream = model.generate_response()
        st.write_stream(response_stream)
# --------------------------------------------------------------------- #