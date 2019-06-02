# https://pynamodb.readthedocs.io/en/latest/low_level.html
# Creating a connection

# Creating a connection is simple
from pynamodb.connection import Connection

conn = Connection()

# You can specify a different DynamoDB url
conn = Connection(host='http://alternative-domain/')

# By default, PynamoDB will connect to the us-east-1 region, but you can specify a different one.
conn = Connection(region='us-west-1')

# Modifying tables


# You can easily list tables:
conn.list_tables()

# or delete a table:

# conn.delete_table('Thread')

# If you want to change the capacity of a table, that can be done as well:

conn.update_table('Thread', read_capacity_units=20, write_capacity_units=20)

# You can create tables as well, although the syntax is verbose. You should really use the model API instead,
#  but here is a low level example to demonstrate the point:

kwargs = {
    'write_capacity_units': 1,
    'read_capacity_units': 1,
    'attribute_definitions': [
        {
            'attribute_type': 'S',
            'attribute_name': 'key1'
        },
        {
            'attribute_type': 'S',
            'attribute_name': 'key2'
        }
    ],
    'key_schema': [
        {
            'key_type': 'HASH',
            'attribute_name': 'key1'
        },
        {
            'key_type': 'RANGE',
            'attribute_name': 'key2'
        }
    ]
}
conn.create_table('table_name', **kwargs)

# You can also use update_table to change the Provisioned Throughput capacity of Global Secondary Indexes:


kwargs = {
    'global_secondary_index_updates': [
        {
            'index_name': 'index_name',
            'read_capacity_units': 10,
            'write_capacity_units': 10
        }
    ]
}
conn.update_table('table_name', **kwargs)

# Modifying items

# The low level API can perform item operations too, such as getting an item:

conn.get_item('table_name', 'hash_key', 'range_key')

# You can put items as well, specifying the keys and any other attributes:
conn.put_item('table_name', 'hash_key', 'range_key', attributes={'key': 'value'})

# Deleting an item has similar syntax:
conn.delete_item('table_name', 'hash_key', 'range_key')

# AWS Access
# https://pynamodb.readthedocs.io/en/latest/awsaccess.html

'''
PynamoDB uses botocore to interact with the DynamoDB API. Thus, any method of configuration supported by botocore works with PynamoDB. For local development the use of environment variables such as AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY is probably preferable. You can of course use IAM users, as recommended by AWS. In addition EC2 roles will work as well and would be recommended when running on EC2.

As for the permissions granted via IAM, many tasks can be carried out by PynamoDB. So you should construct your policies as required, see the DynamoDB docs for more information.

If for some reason you can’t use conventional AWS configuration methods, you can set the credentials in the Model Meta class:
'''
from pynamodb.models import Model


class MyModel(Model):
    class Meta:
        aws_access_key_id = 'my_access_key_id'
        aws_secret_access_key = 'my_secret_access_key'
