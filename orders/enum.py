from django.db import models

class UnitChoices(models.TextChoices):
    KILO = 'KG', 'Kilo'
    PACK = 'P', 'Pack'
    CASE = 'C', 'Case'
    BOTTLE = 'B', 'Bottle'
    CAN = 'CA', 'Can'
    LITER = 'L', 'Liter'
    BAG = 'BA', 'Bag'
    CANISTER = 'CAN', 'Canister'
    KEG = 'K', 'Keg'
    UNIT = 'U', 'Unit'

