from tortoise import fields, models


class Cargo(models.Model):
    """ Модель груза """

    id = fields.UUIDField(pk=True)
    cargo_type = fields.ForeignKeyField('models.CargoType')
    date_supplied = fields.DateField()
    price = fields.FloatField()
    insurance_price = fields.FloatField()
