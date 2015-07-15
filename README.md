# messages-api

Simple Python Flask api app to serve as backend for a simple messaging system. Uses Neo4j database for persistence.

Demo is running on heroku at `http://messages-api.herokuapp.com`. **NOTE:** The API uses Basic Auth authentication scheme and tokens (as well as database credentials) are not checked into version control.

## API endpoints

### Post a new message

`POST /message`

Example JSON body:

~~~
{
  "content": "Hey there!",
  "receiver": "aflyon",
  "sender": "eddie"
}
~~~

### Get all message threads for a user

Returns list of users and the number of messages in each thread 

`GET /<username>/conversations`

Example JSON response:

~~~
{
    "threads": [
        {
            "count": 4,
            "username": "lyonwj"
        },
        {
            "count": 2,
            "username": "eddie"
        }
    ]
}
~~~

### Get a conversation for a user pair (a single thread)

Return an list of messages, each with `content`, `datetime` and `sender` properties. Messages are returned in descending chronological order.

`GET /<username>/conversations/<other_user>`

Example JSON response:

~~~
{
  "messages": [
    {
      "content": "Or Maybe dinner?",
      "datetime": 1436992088654,
      "sender": "lyonwj"
    },
    {
      "content": "Wanna grab a coffee?",
      "datetime": 1436991212252,
      "sender": "lyonwj"
    },
    {
      "content": "Hi! Nice to meet you!",
      "datetime": 1436923827609,
      "sender": "lyonwj"
    },
    {
      "content": "Hey there!",
      "datetime": 1436923813549,
      "sender": "aflyon"
    }
  ]
}
~~~