import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = "/home/xioahei/Learning/MockRiksdagAPI/"

connex_app = connexion.App(__name__, specification_dir=basedir)
flask_app = connex_app.app
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + \
        os.path.join(basedir, 'transcripts.db')

flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(flask_app)
ma = Marshmallow(flask_app)
