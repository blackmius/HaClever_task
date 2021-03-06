from tortoise import fields, models


class CargoType(models.Model):
    """ Модель типа груза """

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=256, unique=True,
                            index=True, null=False)
