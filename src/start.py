from pynamodb.models import Model
from pynamodb.connection import Connection
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute
)
from project_setting import DB_HOST, REGION


# https://pynamodb.readthedocs.io/en/latest/quickstart.html
class UserModel(Model):
    """
    A DynamoDB User
    """

    class Meta:
        table_name = 'dynamodb-user'
        host = DB_HOST
        region = REGION
        write_capacity_units = 1
        read_capacity_units = 1

    email = UnicodeAttribute(hash_key=True)
    first_name = UnicodeAttribute(null=True)
    last_name = UnicodeAttribute(null=True)


if not UserModel.exists():
    UserModel.create_table()

user = UserModel('test@example.com', first_name='Samuel', last_name='Adams')

user.save()
n = UserModel.count()
print(n)

# Did another process update the user? We can refresh the user with data from DynamoDB
user.refresh()

user = UserModel.get('test@example.com')
user.first_name = 'Robert'
user.save()
pass
