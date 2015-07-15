from py2neo import Graph

# Neo4j Cypher queries

SEND_MESSAGE_QUERY = '''
    MERGE (sender:User {name: {sender}})
    MERGE (receiver:User {name: {receiver}})
    CREATE (sender)-[:SENT]->(m:Message)-[:TO]->(receiver)
    SET m.content = {content},
        m.datetime = timestamp(),
        m.sender = {sender}
'''

CONVERSATIONS_QUERY = '''
    MATCH (u:User {name: {username}})
    MATCH (u)-[r]-(m:Message)-[]-(u2)
    WITH u2, count(r) as numMessages
    RETURN u2.name as user, numMessages
'''

MESSAGE_PAIR_QUERY = '''
    MATCH (u:User {name: {user} })
    MATCH (u2:User {name: {other_user} })
    MATCH (u)-[]-(m:Message)-[]-(u2)
    WITH m.sender AS sender, m.content AS content, m.datetime AS datetime
    RETURN sender, content, datetime ORDER BY datetime DESC
'''


class Neo4jInterface:
    def __init__(self, db_url):
        self.db = Graph(db_url)

    def sendMessage(self, message):
        params = {}
        params['sender'] = message.get('sender')
        params['receiver'] = message.get('receiver')
        params['content'] = message.get('content')

        res = self.db.cypher.execute(SEND_MESSAGE_QUERY, params)

        return {'status': 'OK'}

    def getConversations(self, user):
        params = {
            "username": user
        }
        res = self.db.cypher.execute(CONVERSATIONS_QUERY, params)
        threads = []
        for item in res:
            thread = {}
            thread['username'] = item.user
            thread['count'] = item.numMessages
            threads.append(thread)

        return {'threads': threads}

    def getConversation(self, user, other_user):
        params = {
            "user": user,
            "other_user": other_user
        }

        res = self.db.cypher.execute(MESSAGE_PAIR_QUERY, params)
        messages = []
        for item in res:
            message = {}
            message['content'] = item.content
            message['sender'] = item.sender
            message['datetime'] = item.datetime

            messages.append(message)

        return {'messages': messages}