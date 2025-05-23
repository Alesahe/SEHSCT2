from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from urllib.parse import urlparse
import user_management as dbHandler
# Code snippet for logging a message
# app.logger.critical("message")

app = Flask(__name__)
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

localDomain = urlparse("/index").netloc

@app.after_request
def applyCSP(response):
    response.headers['Content-Security-Policy'] = "base-uri 'self'; default-src 'self'; style-src 'self'; script-src 'self'; media-src 'self'; font-src 'self'; object-src 'self'; child-src 'self'; connect-src 'self'; worker-src 'self'; report-uri '/csp_report'; frame-ancestors 'none'; form-action 'self'; frame-src 'none';"
    return response

@app.route("/success.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def addFeedback():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url")
        parsedURL = urlparse(url)
        if parsedURL.netloc != localDomain or  urlparse(url).scheme: 
            return redirect("/index", code=302)
        else:
            return redirect(url, code=302)
    if request.method == "POST":
        feedback = request.form["feedback"]
        dbHandler.insertFeedback(feedback)
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")
    else:
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")


@app.route("/signup.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url")
        parsedURL = urlparse(url)
        if parsedURL.netloc != localDomain or  urlparse(url).scheme: 
            return redirect("/index", code=302)
        else:
            return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        DoB = request.form["dob"]
        dbHandler.insertUser(username, password, DoB)
        return render_template("/index.html")
    else:
        return render_template("/signup.html")


@app.route("/index.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
@app.route('/', methods=['POST', 'GET'])

def home():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url")
        parsedURL = urlparse(url)
        if parsedURL.netloc != localDomain or  urlparse(url).scheme: 
            return redirect("/index", code=302)
        else:
            return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        isLoggedIn = dbHandler.retrieveUsers(username, password)
        if isLoggedIn:
            dbHandler.listFeedback()
            return render_template("/success.html", value=username, state=isLoggedIn)
        else:
            return render_template("/index.html")
    else:
        return render_template("/index.html")


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=5000)
