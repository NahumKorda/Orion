import base64
import os
import time
from datetime import datetime
from pathlib import Path

import streamlit as st

from agents.qna.crew import QuestionAnsweringCrew
from ui.pdf import create_pdf
from utils.pdf_reader import get_text


def show_insights_screen():
    # Consolidate all CSS styling into a single markdown element
    st.markdown("""
    <style>
        /* Remove default Streamlit padding and margins */
        .block-container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            padding-left: 5% !important; /* Add 5% left margin */
            padding-right: 5% !important; /* Add 5% right margin */
            margin-top: 0 !important;
            max-width: 90% !important; /* Set max width to 90% */
            width: 90% !important; /* Set width to 90% */
            height: 100vh !important; /* Make container fill viewport height */
        }
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}

        /* Remove any top borders or lines */
        .main .block-container::before {
            content: none !important;
            border: none !important;
            margin: 0 !important;
            padding: 0 !important;
            height: 0 !important;
        }

        /* Remove extra padding at the very top */
        [data-testid="stAppViewContainer"] > div:first-child {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }

        /* Header styling */
        h1 {
            margin-top: 0 !important;
            padding-top: 0 !important;
            margin-bottom: 0.25rem !important;
            padding-bottom: 0 !important;
            display: inline-block !important;
        }

        /* Header container styling */
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 !important;
            margin: 0 !important;
            margin-bottom: 0 !important; /* Remove space between header and panels */
        }

        /* Button container styling */
        .button-container {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            gap: 10px;
        }

        /* Style for buttons */
        /* Fix spacing for header columns */
        [data-testid="stHorizontal"] > div:first-child {
            padding-right: 0 !important;
        }

        /* Align buttons to the right */
        .header-right-col {
            display: flex;
            justify-content: flex-end;
            padding: 0 !important;
            margin: 0 !important;
        }

        /* CRITICAL - Make panels take up full space */
        [data-testid="stVerticalBlock"] {
            height: calc(100vh - 100px) !important;
        }

        [data-testid="stHorizontal"] {
            height: calc(100vh - 150px) !important;
        }

        /* Make columns fill vertical space */
        [data-testid="column"] {
            height: calc(100vh - 150px) !important;
        }

        /* New specialized classes for iframe containers */
        .report-iframe-container {
            height: calc(100vh - 131px) !important; /* Reduced height to make room for text input */
            margin: 0 !important;
            padding: 0 !important;
            border: 1px solid #ddd;
            border-radius: 5px;
            overflow: hidden;
            display: block;
            margin-bottom: 10px !important;
        }

        .chat-iframe-container {
            height: calc(100vh - 220px) !important; /* Reduced height to make room for text input */
            margin: 0 !important;
            padding: 0 !important;
            border: 1px solid #ddd;
            border-radius: 5px;
            overflow: hidden;
            display: block;
            margin-bottom: 10px !important;
        }

        /* Basic message styling */
        .user-message {
            background-color: #e0e0e0;
            border-radius: 15px 15px 15px 0;
            padding: 8px 12px;
            margin: 5px 0;
            max-width: 80%;
            float: left;
            clear: both;
        }
        .assistant-message {
            background-color: #1E4D8C;
            color: white;
            border-radius: 15px 15px 0 15px;
            padding: 8px 12px;
            margin: 5px 0;
            max-width: 80%;
            float: right;
            clear: both;
        }

        /* Consistent iframe styling */
        .report-iframe-container iframe,
        .chat-iframe-container iframe {
            width: 100%;
            height: 100%;
            border: none;
            margin: 0 !important;
            padding: 0 !important;
            display: block;
        }

        /* Clear floats */
        .clearfix:after {
            content: "";
            display: table;
            clear: both;
        }

        /* Position indicator styling */
        .stTabs [data-baseweb="tab-panel"] .stMarkdown p {
            margin-top: 5px !important;
        }

        /* Fix spacing for text input label */
        [data-testid="stTextInput"] label {
            margin-top: 0 !important;
            padding: 0 !important;
            position: relative !important;
        }

        /* Fix the text input styling */
        [data-testid="stTextInput"] {
            margin-top: 10px !important;
            padding-top: 0 !important;
            position: relative !important;
            color: rgb(0, 0, 0);
        }

        /* Make text input visible and properly positioned */
        [data-testid="stTextInput"] > div > div > input {
            background-color: white !important;
            border: 1px solid #ddd !important;
            border-radius: 5px !important;
            color: black !important;  /* Changed from white to black */
        }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state variables if they don't exist
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    if 'current_html_index' not in st.session_state:
        st.session_state.current_html_index = {'Quantitative results': 0, 'Qualitative results': 0}
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Quantitative results"
    if 'session_id' not in st.session_state:
        st.session_state.session_id = int(time.time() * 1000)

    current_path = Path(__file__).resolve()
    package_root = current_path.parent.resolve()
    parent_root = package_root.parent.resolve()
    project_root = parent_root.parent.resolve()
    data_path = os.path.join(project_root, "data")

    # Initialize HTML Assistant if it doesn't exist yet
    if 'qna_agent' not in st.session_state:
        report_path = os.path.join(data_path, "100 Days into Trump's 2nd Term.pdf")
        if os.path.exists(report_path):
            st.session_state.report_text = get_text(report_path)
            print(st.session_state.report_text)
            st.session_state.qna_agent = QuestionAnsweringCrew().crew()

    # Sample HTML files for demonstration (replace with actual file paths)
    if 'html_files' not in st.session_state:
        st.session_state.html_files = {
            'Quantitative results': [
                os.path.join(data_path, "quantitative/01.html"),
                os.path.join(data_path, "quantitative/02.html"),
                os.path.join(data_path, "quantitative/03.html"),
                os.path.join(data_path, "quantitative/04.html"),
                os.path.join(data_path, "quantitative/05.html"),
                os.path.join(data_path, "quantitative/06.html"),
            ],
            'Qualitative results': [
                os.path.join(data_path, "qualitative/01.html"),
                os.path.join(data_path, "qualitative/02.html"),
                os.path.join(data_path, "qualitative/03.html"),
                os.path.join(data_path, "qualitative/04.html"),
                os.path.join(data_path, "qualitative/05.html"),
                os.path.join(data_path, "qualitative/06.html"),
                os.path.join(data_path, "qualitative/07.html"),
            ]
        }

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
                with st.spinner("Thinking..."):
                    try:
                        inputs = {
                            'report': st.session_state.report_text,
                            'question': user_question
                        }
                        response = st.session_state.qna_agent.kickoff(inputs)
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
            report_file = os.path.join(data_path, "report.html")

            try:
                if os.path.exists(report_file):
                    with open(report_file, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                else:
                    html_content = f"<html><body><h2>File not found</h2><p>Could not locate: {report_file}</p></body></html>"
            except Exception as e:
                html_content = f"<html><body><h2>Error loading file</h2><p>{str(e)}</p></body></html>"

            simple_html = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                <style>
                    html, body {{
                        height: 100%;
                        margin: 0;
                        padding: 0;
                        overflow: hidden;
                    }}
                    .scrollable-container {{
                        height: 100%;
                        width: 100%;
                        overflow-y: auto;
                        overflow-x: auto;
                        box-sizing: border-box;
                    }}
                    .content-wrapper {{
                        padding: 20px;
                        min-height: 100%;
                        box-sizing: border-box;
                        /* Center the content horizontally */
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                    }}
                    /* In case the content itself needs specific centering */
                    .content-wrapper > * {{
                        max-width: 100%;
                    }}
                </style>
            </head>
            <body>
                <div class="scrollable-container">
                    <div class="content-wrapper">
                        {html_content}
                    </div>
                </div>
            </body>
            </html>
            """

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
                        "content": "Hello! I'm your Orion assistant. I can help answer questions about the HTML content you're viewing. What would you like to know?",
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })

                # Build chat messages HTML
                messages_html = ""
                for message in st.session_state.chat_messages:
                    if message["role"] == "user":
                        messages_html += f"""
                        <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                            <div style="background-color: #e0e0e0; color: black; padding: 8px 12px; 
                                 border-radius: 15px 15px 0 15px; max-width: 80%; text-align: right; word-wrap: break-word;
                                 font-family: Arial, sans-serif;">
                                {message['content']}
                            </div>
                        </div>
                        """
                    else:
                        messages_html += f"""
                        <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                            <div style="background-color: #1E4D8C; color: white; padding: 8px 12px; 
                                 border-radius: 15px 15px 15px 0; max-width: 80%; text-align: left; word-wrap: break-word;
                                 font-family: Arial, sans-serif;">
                                {message['content']}
                            </div>
                        </div>
                        """

                # Create a full HTML component with proper height settings for chat
                chat_html = f"""
                <!DOCTYPE html>
                <html style="height: 100%; margin: 0; padding: 0;">
                <head>
                    <style>
                        html, body {{
                            height: 100%;
                            margin: 0;
                            padding: 0;
                            overflow: hidden;
                            font-family: Arial, sans-serif;
                        }}
                        body {{
                            display: flex;
                            flex-direction: column;
                            font-family: Arial, sans-serif;
                        }}
                        #chat-container {{
                            flex: 1;
                            display: flex;
                            flex-direction: column;
                            height: 100%;
                            overflow: hidden;
                            padding: 10px;
                            font-family: Arial, sans-serif;
                        }}
                        #empty-space {{
                            flex-grow: 1;
                        }}
                        #messages {{
                            overflow-y: auto;
                            font-family: Arial, sans-serif;
                        }}
                        .user-message, .assistant-message {{
                            font-family: Arial, sans-serif;
                        }}
                    </style>
                </head>
                <body>
                    <div id="chat-container">
                        <div id="empty-space"></div>
                        <div id="messages">
                            {messages_html}
                        </div>
                    </div>

                    <script>
                        // Function to scroll to bottom of chat
                        function scrollToBottom() {{
                            const messageContainer = document.getElementById('messages');
                            if (messageContainer) {{
                                messageContainer.scrollTop = messageContainer.scrollHeight;
                            }}
                        }}

                        // Scroll when loaded and after delays
                        window.onload = function() {{
                            scrollToBottom();
                            setTimeout(scrollToBottom, 100);
                            setTimeout(scrollToBottom, 500);
                        }};
                    </script>
                </body>
                </html>
                """

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