import gradio as gr
from chatbot import chatbot_response

chat_history = []

def chat_interface(user_message):
    global chat_history

    response = chatbot_response(user_message)
    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "assistant", "content": response})

    return chat_history

with gr.Blocks(css="""
    .gradio-container { font-family: 'Arial', sans-serif; }
    .gr-button { 
        background-color: #4CAF50; 
        color: white; 
        font-size: 16px; 
        padding: 12px 20px; 
        border-radius: 25px; 
        border: none;
        cursor: pointer;
    }
    .gr-button:hover { background-color: #45a049; }
    .gr-button:active { background-color: #2e8b47; }
    .gr-textbox { border-radius: 25px; }
    .gr-chatbot { max-height: 400px; overflow-y: scroll; }
    .gr-textbox input { font-size: 16px; padding: 10px; }
""") as demo:

    chatbot_ui = gr.Chatbot()
    user_input = gr.Textbox(label="Your Message", placeholder="Type your message here...")
    submit_button = gr.Button("Send")

    def on_submit(user_text):
        return chat_interface(user_text)

    submit_button.click(on_submit, inputs=[user_input], outputs=[chatbot_ui])
    user_input.submit(on_submit, inputs=[user_input], outputs=[chatbot_ui])

demo.launch()
