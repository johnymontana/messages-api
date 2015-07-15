from flask import Flask, jsonify, make_response, request
from flask.ext.httpauth import HTTPBasicAuth
from neo4jInterface import Neo4jInterface
import config

app = Flask(__name__)
auth = HTTPBasicAuth()


neo4jInterface = Neo4jInterface(config.DB_URL)

# basic auth authentication

@auth.get_password
def get_password(username):
    if username == config.USERNAME:
        return config.PASSWORD
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized'}), 401)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

# Post a new message
@app.route('/message', methods=['POST'])
@auth.login_required
def post_message():
    message = request.get_json()
    result = neo4jInterface.sendMessage(message)
    return jsonify(result)

# Get all conversations for a particular user
# Returns an array of users and message count (the number of messages exchanged)
# If message count is > 0, also returns a datetime of the last message exchanged
@app.route('/<string:username>/conversations', methods=['GET'])
@auth.login_required
def get_conversations(username):
    conversations = neo4jInterface.getConversations(username)
    return jsonify(conversations)

# Get a conversation (message history) for a specific user pair
# Returns an array of messages (content, user, and datetime)
@app.route('/<string:username>/conversations/<string:other_user>', methods=['GET'])
def get_conversation_for_user_pair(username, other_user):
    conversation = neo4jInterface.getConversation(username, other_user)
    return jsonify(conversation)


if __name__ == '__main__':
    app.run()
