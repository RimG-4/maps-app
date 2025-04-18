from app.utils.db import db


class T_Feedback(db.Model):
    __tablename__ = 'T_Feedback'

    feedbackID = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('T_User.userID'))
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

    user = db.relationship('T_User', backref='feedbacks')