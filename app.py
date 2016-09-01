from flask import Flask, request
from time import sleep
app = Flask(__name__)


@app.route("/", methods=['GET'])
def home_get():
	return "GET is working\n"


@app.route("/", methods=['POST'])
def home_post():
	sleep(5)
	j = str(request.get_json(force=True))
	return "POST is working\n%s\n" % j


if __name__ == "__main__":
	app.run(host='0.0.0.0')
