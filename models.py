from config import db
#db.metadata.clear()
class Transcript(db.Model):
    __tablename__ = "transcript"
    transcript_id = db.Column(db.String(30), primary_key=True)
    transcript = db.Column(db.UnicodeText)
    speaker_id = db.Column(db.String(20))
    speaker_title = db.Column(db.String(32))
    party = db.Column(db.String(2))
    section = db.Column(db.String(100))
    date = db.Column(db.String(30))
