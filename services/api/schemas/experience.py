from ma import ma
from models.experience import ExperienceModel


class ExperienceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ExperienceModel
        include_fk = True
        load_instance = True
        dump_only = ("id",)
