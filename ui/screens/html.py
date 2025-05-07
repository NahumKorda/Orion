def reduced_title_padding():
    return """
        <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
        h1 {
            margin-top: 0rem;
        }
        </style>
    """


def get_simple_html(html_content: str) -> str:
    return f"""
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


def get_user_bubble(content: str) -> str:
    return f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                <div style="background-color: #e0e0e0; color: black; padding: 8px 12px; 
                     border-radius: 15px 15px 0 15px; max-width: 80%; text-align: right; word-wrap: break-word;
                     font-family: Arial, sans-serif;">
                    {content}
                </div>
            </div>
            """


def get_response_bubble(content: str) -> str:
    return f"""
            <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                <div style="background-color: #1E4D8C; color: white; padding: 8px 12px; 
                     border-radius: 15px 15px 15px 0; max-width: 80%; text-align: left; word-wrap: break-word;
                     font-family: Arial, sans-serif;">
                    {content}
                </div>
            </div>
            """

def get_chat(messages: str) -> str:
    return f"""
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
                            {messages}
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


def get_insights_css() -> str:
    return """
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
            color: rgb(0, 0, 0) !important;
            caret-color: rgb(0, 0, 0) !important;
        }
        
        input.st-dc {
            color: rgb(0, 0, 0) !important;
            caret-color: rgb(0, 0, 0) !important;
        }

        /* Make text input visible and properly positioned */
        [data-testid="stTextInput"] > div > div > input {
            background-color: white !important;
            border: 1px solid #ddd !important;
            border-radius: 5px !important;
            color: black !important;  /* Changed from white to black */
        }
    </style>
    """
