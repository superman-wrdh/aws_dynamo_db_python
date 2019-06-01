from pynamodb.indexes import LocalSecondaryIndex, AllProjection
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute,
)
from project_setting import DB_HOST, REGION
from datetime import datetime
from create_data import user_data


class PhoneIndex(LocalSecondaryIndex):
    """
    This class represents a local secondary index
    """

    class Meta:
        # All attributes are projected
        projection = AllProjection()

    no = UnicodeAttribute(hash_key=True)
    phone = UnicodeAttribute(range_key=True)


class ZipCodeIndex(LocalSecondaryIndex):
    """
    This class represents a local secondary index
    """

    class Meta:
        # All attributes are projected
        projection = AllProjection()

    no = UnicodeAttribute(hash_key=True)
    zipcode = UnicodeAttribute(range_key=True)


class User(Model):
    class Meta:
        table_name = 'user'
        host = DB_HOST
        region = REGION
        write_capacity_units = 1
        read_capacity_units = 1

    no = UnicodeAttribute(hash_key=True)
    first_name = UnicodeAttribute(range_key=True)
    last_name = UnicodeAttribute(null=True)
    birthday = UTCDateTimeAttribute(null=True)
    phone = UnicodeAttribute(null=True)
    state = UnicodeAttribute(null=True)
    zipcode = UnicodeAttribute(null=True)
    email = UnicodeAttribute(null=True)

    phone_index = PhoneIndex()
    zipcode_index = ZipCodeIndex()


def create_data():
    if not User.exists():
        User.create_table()
    for data in user_data:
        # {'birthday' 'email''first_name''last_name''no': 'phone''state''zipcode'}
        date_value = data.get("birthday")
        data["birthday"] = datetime(date_value.year, date_value.month, date_value.day)
        user = User(**data)
        user.save()

    print("数据总数", User.count())


# create_data()

def index_query():
    for u1 in User.phone_index.query("0"):
        print(u1.no, u1.first_name, u1.last_name)
    print(list(User.phone_index.query("1", limit=1)))


if __name__ == '__main__':
    index_query()
