import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = "/home/xioahei/Learning/MockRiksdagAPI/"

connex_app = connexion.App(__name__, specification_dir=basedir)
app = connex_app.app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + \
        os.path.join(basedir, 'transcripts.db')

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)
