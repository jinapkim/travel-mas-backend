from ma import ma

from models.image import ImageModel


class ImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ImageModel
        include_relationships = True
        load_instance = True
        dump_only = ("id",)
