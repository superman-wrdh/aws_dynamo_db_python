# https://pynamodb.readthedocs.io/en/latest/batch.html
# Query Filters
# You can query items from your table using a simple syntax:
from project_setting import User
from datetime import datetime

for item in User.query('2', User.first_name.startswith('a')):
    print("Query returned item {0}".format(item))

# Additionally, you can filter the results before they are returned using condition expressions:
for item in User.query('3', User.first_name == 'Subject', User.views > 0):
    print("Query returned item {0}".format(item))

# DynamoDB only allows the following conditions on range keys:
#  ==, <, <=, >, >=, between, and startswith.
# DynamoDB does not allow multiple conditions using range keys.


# Scan Filters
# Scan filters have the same syntax as Query filters, but support all condition expressions:
for item in User.scan(User.last_name.startswith('Re') & (User.birthday > datetime(1991, 2, 1))):
    print(item)

# Limiting results
# Both Scan and Query results can be limited to a maximum number of items using the limit argument.

for item in User.query('66', User.first_name.startswith('Mi'), limit=5):
    print("Query returned item {0}".format(item))
