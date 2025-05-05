import base64
import os
import time
from datetime import datetime

import markdown
import streamlit as st

from agents.qna.crew import QuestionAnsweringCrew
from ui.pdf import create_pdf
from ui.screens.html import get_simple_html, get_user_bubble, get_response_bubble, get_chat, get_insights_css
from ui.utils import get_data_path
from utils.pdf_reader import get_text


def show_insights_screen():
    # Consolidate all CSS styling into a single markdown element
    st.markdown(get_insights_css(), unsafe_allow_html=True)

    # Initialize session state variables if they don't exist
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    if 'session_id' not in st.session_state:
        st.session_state.session_id = int(time.time() * 1000)

    # Initialize HTML Assistant if it doesn't exist yet
    if 'qna_agent' not in st.session_state:
        report_path = os.path.join(get_data_path(), "100 Days into Trump's 2nd Term.pdf")
        if os.path.exists(report_path):
            st.session_state.report_text = get_text(report_path)
            print(st.session_state.report_text)
            st.session_state.qna_agent = QuestionAnsweringCrew().crew()
    else:
        print("SESSION STATE")
        for key in st.session_state.keys():
            print(key)

    def reset():
        for key in st.session_state.keys():
            del st.session_state[key]

    def send_message():
        if st.session_state.user_input.strip():
            user_question = st.session_state.user_input

            # Add user message to chat
            st.session_state.chat_messages.append({
                "role": "user",
                "content": user_question,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })

            # Get response from HTMLAssistant if it exists
            if st.session_state.qna_agent:
                try:
                    inputs = {
                        'report': st.session_state.report_text,
                        'question': user_question
                    }
                    response = st.session_state.qna_agent.kickoff(inputs)
                    print(response.raw)
                    response = markdown.markdown(response.raw, extensions=['tables', 'fenced_code'])
                except Exception as e:
                    response = f"Sorry, I encountered an error: {str(e)}. Please try again."
            else:
                response = "Sorry, I couldn't analyze the report. Please make sure the report.html file exists in the data directory."

            # Add assistant response to chat
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })

            # Clear input
            st.session_state.user_input = ""

            # Update session ID to force refresh of HTML component
            st.session_state.session_id = int(time.time() * 1000)

    # Create a custom container for the header with minimal margin-bottom
    header_container = st.container()
    with header_container:
        # Create columns for title and buttons
        title_col, buttons_col = st.columns([3, 1], vertical_alignment="center")

        # Add title to the left column
        with title_col:
            st.title("Results")

        # Add buttons to the right column
        with buttons_col:
            # Use columns to place buttons side by side
            btn_cols = st.columns(2, vertical_alignment="center")

            # Download PDF button
            with btn_cols[0]:
                st.download_button(
                    label="Download PDF",
                    data=create_pdf(),
                    file_name="orion_dashboard.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            # New Survey button
            with btn_cols[1]:
                if st.button("New Survey", key="insights_back", use_container_width=True):
                    reset()
                    st.session_state.current_screen = 'survey'
                    st.rerun()

    # Create the main container
    main_container = st.container()
    with main_container:
        # Create two columns for the panels with 70/30 split
        left_col, right_col = st.columns([7, 3])

        # Left Panel - HTML Display
        with left_col:
            # Display a single HTML file (report.html)
            report_file = os.path.join(get_data_path(), "report.html")

            try:
                if os.path.exists(report_file):
                    with open(report_file, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                else:
                    html_content = f"<html><body><h2>File not found</h2><p>Could not locate: {report_file}</p></body></html>"
            except Exception as e:
                html_content = f"<html><body><h2>Error loading file</h2><p>{str(e)}</p></body></html>"

            simple_html = get_simple_html(html_content)

            # Encode the HTML content
            encoded_html = base64.b64encode(simple_html.encode()).decode()

            # Use the report iframe container
            st.markdown(
                f'<div class="report-iframe-container"><iframe src="data:text/html;base64,{encoded_html}"></iframe></div>',
                unsafe_allow_html=True
            )

        # Right Panel - Chat
        with right_col:
            # Chat messages container
            chat_container = st.container()

            # Create a container for the scrollable area
            with chat_container:
                # Add a welcome message if chat is empty
                if not st.session_state.chat_messages:
                    st.session_state.chat_messages.append({
                        "role": "assistant",
                        "content": "Hello! I'm your Orion assistant. I can help answer questions about the report you're viewing. What would you like to know?",
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })

                # Build chat messages HTML
                messages_html = ""
                for message in st.session_state.chat_messages:
                    if message["role"] == "user":
                        messages_html += get_user_bubble(message['content'])
                    else:
                        messages_html += get_response_bubble(message['content'])

                # Create a full HTML component with proper height settings for chat
                chat_html = get_chat(messages_html)
                # Create a data URL for the chat content
                chat_data_url = f"data:text/html;base64,{base64.b64encode(chat_html.encode()).decode()}"

                # Display using the chat iframe container
                st.markdown(
                    f'<div class="chat-iframe-container"><iframe src="{chat_data_url}"></iframe></div>',
                    unsafe_allow_html=True
                )

                # Chat input area - MOVED INSIDE the chat_container to position it below the iframe
                st.text_input("Ask questions about the results:", key="user_input", on_change=send_message,
                              placeholder="Type your question here...")