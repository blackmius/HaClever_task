from tortoise import fields, models


class Tarrif(models.Model):
    """ Tarrif Model """

    id = fields.UUIDField(pk=True)
    cargo_type = fields.ForeignKeyField('models.CargoType')
    date = fields.DateField()
    rate = fields.FloatField()
