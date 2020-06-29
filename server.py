import os
from flask import render_template
import config


connex_app = config.connex_app
connex_app.add_api("ParlSpeeches.yml")
@connex_app.route("/")
def homepage():
    return render_template("homepage.html")
if __name__ == "__main__":
    connex_app.run(debug=True)
