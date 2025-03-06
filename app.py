from flask import Flask, render_template, send_file
from flask_socketio import SocketIO, emit
import os
from dotenv import load_dotenv
import utils.openai_utils as openai_utils
from utils.chat_manager import ChatManager
import uuid
import time

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')
socketio = SocketIO(app, ping_timeout=360, ping_interval=30)
# Create the openai client
openai_utils.create_client()
openai_utils.create_image_client()
# Create the chat manager
chat_manager = ChatManager()

@app.route('/')
def index():
    """Serves the main HTML page."""
    chat_manager.clear_conversation()
    return render_template('index.html')

@app.route('/get_image/<image_name>')
def get_image(image_name):
    """Serve the generated image to the client."""
    image_path = os.path.join("static", "img", image_name)
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png')
    else:
        print(f"File not found: {image_path}")
        return send_file(os.path.join("static", "img", "book-cover.png"), mimetype='image/png')

@socketio.on('connect')
def test_connect():
    """Handles client connection."""
    print('Client connected')
    emit('my response', {'data': "Let's start a magical adventure! What's yout name?", "new_image":"book-cover.png"})

@socketio.on('disconnect')
def test_disconnect():
    """Handles client disconnection."""
    print('Client disconnected')

@socketio.on('my event')
def handle_my_custom_event(json):
    """Handles custom event 'my event'."""
    print('received json: ' + str(json))
    # Get the user message
    user_message = json['data']
    # add the user message to the history
    chat_manager.add_user_message(user_message)
    # Get the conversation history
    conversation = chat_manager.get_conversation_history()
    # Generate the openAI response
    openai_response = openai_utils.generate_response(conversation)
    # add the ai message to the history
    chat_manager.add_ai_message(openai_response)
    # create the image prompt
    image_prompt = openai_utils.create_image_prompt(openai_response)
    #generate the image
    new_image_name = f"{uuid.uuid4()}.png"
    # Wait for the image to be created
    openai_utils.generate_image(new_image_name, image_prompt)
    # add the new image to the manager
    chat_manager.set_new_image(new_image_name)
    #Send the response to the client.
    emit('my response', {'data': openai_response, "new_image":new_image_name})

if __name__ == '__main__':
    socketio.run(app, debug=True)
