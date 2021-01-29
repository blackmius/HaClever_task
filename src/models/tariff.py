from tortoise import fields, models


class Tariff(models.Model):
    """ Модель тарифа """

    id = fields.UUIDField(pk=True)
    cargo_type = fields.ForeignKeyField('models.CargoType')
    date = fields.DateField(index=True)
    rate = fields.FloatField()
