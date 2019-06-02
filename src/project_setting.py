from pynamodb.indexes import LocalSecondaryIndex, AllProjection
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute,
)

DB_HOST = "http://192.168.199.199:8000"
REGION = "us-west-1"


def list_table():
    from pynamodb.connection import Connection
    conn = Connection(host=DB_HOST, region=REGION)
    tables = conn.list_tables()
    print(tables)
    return tables


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


if __name__ == '__main__':
    list_table()
