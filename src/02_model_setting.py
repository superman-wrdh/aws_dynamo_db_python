from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute
)

# https://pynamodb.readthedocs.io/en/latest/tutorial.html
"""
The table that your model represents must exist before you can use it. 
It can be created in this example by calling Thread.create_table(…).
 Any other operation on a non existent table will cause a TableDoesNotExist exception to be raised.
"""


class Thread(Model):
    class Meta:
        table_name = 'Thread'

    forum_name = UnicodeAttribute(hash_key=True)
    subject = UnicodeAttribute(range_key=True)
    views = NumberAttribute(default=0)
    replies = NumberAttribute(default=0)
    answered = NumberAttribute(default=0)
    tags = UnicodeSetAttribute()
    last_post_datetime = UTCDateTimeAttribute()


"""
All DynamoDB tables have a hash key, and you must specify which attribute is the hash key for each Model
 you define. The forum_name attribute 
 in this example is specified as the hash key for this table with the hash_key argument;
  similarly the subject attribute is specified as the range key with the range_key argument.
"""

# Model Settings
"""
The Meta class is required with at least the table_name class attribute to tell the model which DynamoDB table to use
 - Meta can be used to configure the model in other ways too. You can specify which DynamoDB region to use with the region, 
 and the URL endpoint for DynamoDB can be specified using the host attribute. 
You can also specify the table’s read and write capacity by adding read_capacity_units and write_capacity_units attributes.
"""


class Thread(Model):
    class Meta:
        table_name = 'Thread'
        # Specifies the region
        region = 'us-west-1'
        # Optional: Specify the hostname only if it needs to be changed from the default AWS setting
        host = 'http://localhost'
        # Specifies the write capacity
        write_capacity_units = 10
        # Specifies the read capacity
        read_capacity_units = 10

    forum_name = UnicodeAttribute(hash_key=True)


# Defining Model Attributes

"""
A Model has attributes, which are mapped to attributes in DynamoDB.
 Attributes are responsible for serializing/deserializing values to a format that DynamoDB accepts,
  optionally specifying whether or not an attribute may be empty using the null argument,
 and optionally specifying a default value with the default argument. You can specify a default value for any field, 
 and default can even be a function.
"""


# NOTE
# DynamoDB will not store empty attributes. By default,
# an Attribute cannot be None unless you specify null=True in the attribute constructor.

class Thread(Model):
    class Meta:
        table_name = 'Thread'

    forum_name = UnicodeAttribute(hash_key=True, default='My Default Value')


# Here is an example of an attribute that can be empty:
class Thread(Model):
    class Meta:
        table_name = 'Thread'

    forum_name = UnicodeAttribute(hash_key=True)
    my_nullable_attribute = UnicodeAttribute(null=True)


# By default, PynamoDB assumes that the attribute name used on a Model has the same name in DynamoDB.
# For example, if you define a UnicodeAttribute called ‘username’ then PynamoDB will use ‘username’ as the field name
#  for that attribute when interacting with DynamoDB. If you wish to have custom attribute names, they can be overidden.
# One such use case is the ability to use human readable attribute names in PynamoDB that are stored in DynamoDB using shorter, terse attribute to save space.

class Thread(Model):
    class Meta:
        table_name = 'Thread'

    forum_name = UnicodeAttribute(hash_key=True)
    # This attribute will be called 'tn' in DynamoDB
    thread_name = UnicodeAttribute(null=True, attr_name='tn')  # tn is real name


# PynamoDB comes with several built in attribute types for convenience, which include the following:
from pynamodb.attributes import NumberSetAttribute, BinaryAttribute, BinarySetAttribute, BooleanAttribute, \
    JSONAttribute, MapAttribute

UnicodeAttribute
UnicodeSetAttribute
NumberAttribute
NumberSetAttribute
BinaryAttribute
BinarySetAttribute
UTCDateTimeAttribute
BooleanAttribute
JSONAttribute
MapAttribute

# Creating the table
if not Thread.exists():
    Thread.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

# Deleting a table
Thread.delete_table()
