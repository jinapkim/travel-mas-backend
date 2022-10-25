from __future__ import annotations
from typing import List, Dict
from db import db


class ImageModel(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(), nullable=False)

    experience = db.relationship("ExperienceModel", backref="experience", lazy="select", uselist=False)

    @classmethod
    def find_by_id(cls, _id: int) -> ImageModel:
        return cls.query.get(_id)

    @classmethod
    def find_by_url(cls, _url: str) -> ImageModel:
        return cls.query.filter_by(url=_url).first()

    @classmethod
    def find_all(cls) -> List[ImageModel]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update_entry(self) -> None:
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def to_dict(self) -> Dict[str, int | str | None]:
        return {
            "id": self.id,
            "url": self.url
        }
