from flask import Flask


app = Flask(__name__)


@app.route("/home", methods=["GET", "POST"])
def index():
    print("CI/CD pipeline established")


if __name__ == "__main__":
    app.run(debug=True)