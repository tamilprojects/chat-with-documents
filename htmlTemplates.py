css = '''
<style>
.chat-message {
    display: flex; 
    align-items: flex-start; 
    margin-bottom: 1.5rem; 
    position: relative; /* To position the message bubble tail */
}
.chat-message.user {
    justify-content: flex-start;
}
.chat-message.bot {
    justify-content: flex-start;
}
.chat-message .avatar {
    width: 15%;
    display: flex;
    justify-content: center;
}
.chat-message .avatar img {
    max-width: 50px;
    max-height: 50px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #ffffff;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
}
.chat-message .message {
    max-width: 80%;
    padding: 1rem;
    border-radius: 0.75rem;
    color: #eaeaea;
    font-size: 1rem;
    line-height: 1.5;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    position: relative;
}
.chat-message.user .message {
    background-color: #2e3a4e; /* Dark blue-gray for user */
    border-top-left-radius: 0; /* Add visual distinction */
}
.chat-message.bot .message {
    background-color: #4a5568; /* Slightly lighter gray for bot */
    border-top-right-radius: 0; /* Add visual distinction */
    margin-top: 0.5rem;
}
/* Tail for the bot message bubble */
.chat-message.bot .message:after {
    content: '';
    position: absolute;
    top: 10px; /* Position the tail closer to the avatar */
    left: -10px; /* Adjust based on alignment */
    width: 0; 
    height: 0; 
    border-style: solid;
    border-width: 10px 10px 10px 0; /* Creates a triangle */
    border-color: transparent #4a5568 transparent transparent; /* Match the bot message color */
}

body {
    background-color: #1e293b;
    font-family: 'Arial', sans-serif;
    color: #e2e8f0;
    margin: 0;
    padding: 0;
}

/* Header Style */
header {
    background-color: #334155;
    color: #ffffff;
    padding: 1rem;
    border-radius: 0.5rem;
    text-align: center;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}
header h1 {
    font-size: 2rem;
    font-weight: bold;
}
header h1 span {
    color: #38bdf8;
}

/* Sidebar Menu */
.sidebar .subheader {
    color: #38bdf8;
    font-size: 1.5rem;
    margin-bottom: 1rem;
}
.sidebar .title {
    color: #e2e8f0;
    font-size: 1.25rem;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: bold;
}

/* File Uploader */
.sidebar .file-uploader label {
    background-color: #475569;
    color: #e2e8f0;
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;
    display: inline-block;
    cursor: pointer;
    transition: all 0.3s ease;
}
.sidebar .file-uploader label:hover {
    background-color: #64748b;
    color: #0f0e0e;
}

/* Spinner */
.spinner {
    color: #38bdf8;
    font-size: 1rem;
    font-weight: bold;
}

/* Input Field */
.text-input input[type="text"] {
    width: 100%;
    padding: 0.75rem;
    font-size: 1rem;
    color: #e2e8f0;
    background-color: #1e293b;
    border: 2px solid #38bdf8;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.3s ease;
}
.text-input input[type="text"]:focus {
    border-color: #64748b;
    outline: none;
}

/* Buttons */
button {
    background-color: #2e73b3;
    color: #0f0e0e;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    border: none;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
button:hover {
    background-color: #0ea5e9;
}

/* Success Message */
.success {
    background-color: #22c55e;
    color: #0f0e0e;
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;
    font-weight: bold;
    margin-top: 1rem;
    text-align: center;
}

/* Spinner Animation */
.spinner::after {
    content: '⏳ Processing...';
    display: inline-block;
    animation: spinner 1s linear infinite;
}
@keyframes spinner {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/3hGHdM4/a-professional-law-guy.jpg" style="max-height: 60px; max-width: 60px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/Nrf6fCR/handsome-Indian-guy.jpg">
    </div>    
    <div class="message">{{MSG}}</div>
</div>

'''