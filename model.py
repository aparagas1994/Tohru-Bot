from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute

class CharacterModel(Model):
    class Meta:
        table_name = "Characters"
        region = 'us-east-1'

    character_name = UnicodeAttribute(hash_key=True)
    hp = NumberAttribute(attr_name="HP")
    mp = NumberAttribute(attr_name="MP")

