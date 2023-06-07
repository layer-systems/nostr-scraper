from flask import Flask, jsonify, request
import psycopg2
import os
import json

# create a Flask instance
app = Flask(__name__)

# get database credentials from environment variables
# (these variables are set in the docker-compose.yml file)
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_name = os.environ.get("DB_NAME")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_database = os.environ.get("DB_DATABASE")
DEBUG = os.environ.get("DEBUG")

# configure the Postgres connection
conn = psycopg2.connect(
    host=db_host,
    database=db_database,
    user=db_user,
    password=db_password,
)

@app.route('/')
def index():
    data = ["Hello world!"]
    return jsonify({"data": data})

# define an API endpoint
@app.route('/countEvents', methods=['GET'])
def countEvents():
    # hardcoded query
    query = "SELECT count(id) FROM event;"

    # execute query
    cur = conn.cursor()
    cur.execute(query)

    # fetch all rows and convert to list of dicts
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append({
            'countEvents': row[0],
            # add more fields as needed
        })

    # close cursor
    cur.close()

    # return JSON response
    return jsonify({
        'data': data
    })

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"test": "test"})

@app.route('/latestPosts', methods=['GET'])
def latestPosts():
    # hardcoded query
    query = 'SELECT content FROM event WHERE kind = 1 ORDER BY created_at DESC LIMIT 100;'

    # execute query
    cur = conn.cursor()
    cur.execute(query)

    # fetch all rows and convert to list of dicts
    rows = cur.fetchall()
    data = []
    for row in rows:
        content = json.loads(bytes(row[0]).decode('utf8'))
        data.append(content)

    # close cursor
    cur.close()

    # return JSON response
    return jsonify({
        'data': data
    })

@app.route('/getnpubforusername/<username>', methods=['GET'])
def npubforusername(username):
    # username = request.args.get('username')
    assert username == request.view_args['username']

    # query
    query = "SELECT encode(pub_key, 'hex') FROM event WHERE kind = 0 AND content LIKE '%"+username+"%' ORDER BY created_at DESC LIMIT 1;"

    # execute query
    cur = conn.cursor()
    cur.execute(query)

    # fetch all rows and convert to list of dicts
    rows = cur.fetchall()
    data = []
    for row in rows:
        # content = json.loads(bytes(row[0]).decode('hex'))
        pubkey = row[0]
        # data.append({"pubkey":pubkey})
        data.append(pubkey)

    # close cursor
    cur.close()

    # return JSON response
    return jsonify({
        'data': data
    })

if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)