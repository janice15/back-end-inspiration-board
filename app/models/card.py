from app import db
class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(80))
    likes_count = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "likes_count": self.likes_count
        }

    @classmethod
    def from_dict(cls, card_details):
        new_message = cls(
            message=card_details["message"],
            likes_count=card_details["likes_count"]
        )
        return new_message