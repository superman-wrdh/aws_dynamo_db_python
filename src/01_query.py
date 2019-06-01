from pynamodb.models import Model
from pynamodb.connection import Connection
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute
)
from project_setting import DB_HOST, REGION


class UserModel(Model):
    """
    A DynamoDB User
    """

    class Meta:
        table_name = 'dynamodb-user1'
        host = DB_HOST
        region = REGION
        write_capacity_units = 1
        read_capacity_units = 1

    first_name = UnicodeAttribute(hash_key=True)
    last_name = UnicodeAttribute(range_key=True)
    email = UnicodeAttribute()


def create_data():
    UserModel.delete_table()
    if not UserModel.exists():
        UserModel.create_table()
    for first_name, last_name in [("Stephanie", "Miller"), ("Stephanie", "Nelson"), ("Katherine", "Harris"),
                                  ("Mark", "Galvan"), ("Mark", "Friedman"), ("Jacob", "Erickson")]:
        user = UserModel(first_name, last_name=last_name, email=first_name + "@163.com")
        user.save()


# create_data()
n = UserModel.count()
print("data size {}".format(n))
print("query")

for user in UserModel.query('Stephanie'):
    print(user.first_name, user.last_name)

for user in UserModel.query("Stephanie", UserModel.last_name.startswith("M")):
    print("Stephanie startswith M ")
    print(user.first_name, user.last_name)

for user in UserModel.query('Stephanie', UserModel.last_name.startswith('M')):
    print(user)

# Counting Items
print(UserModel.count('Stephanie', UserModel.last_name.startswith('M')))

# Counts also work for indexes:
# print(UserModel.custom_index.count('my_hash_key'))
# print(UserModel.count())

# when hash_key is None raises a ValueError
print(UserModel.count(UserModel.last_name == 'John'))

# returns count of only the matching users
print(UserModel.count('my_hash_key', UserModel.first_name == 'John'))