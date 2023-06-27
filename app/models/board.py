from app import db

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80))
    owner = db.Column(db.String(80))
    cards = db.relationship("Card", back_populates="board")


    def to_dict(self):
        return {
            "board_id": self.id,
            "title": self.title,
            "owner": self.owner
        }

    @classmethod
    def from_dict(cls, board_details):
        new_board = cls(
            title=board_details["title"],
            owner=board_details["owner"]
        )
        return new_board