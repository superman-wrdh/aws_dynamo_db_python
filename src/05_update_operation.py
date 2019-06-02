# https://pynamodb.readthedocs.io/en/latest/updates.html
# Update Operations
# The UpdateItem DynamoDB operations allows you to create or modify attributes
# of an item using an update expression. See the official documentation for more details.

# Suppose that you have defined a Thread Model for the examples below.
from botocore.exceptions import ClientError
from pynamodb.models import Model
from pynamodb.attributes import (
    ListAttribute, UnicodeAttribute, UnicodeSetAttribute, NumberAttribute
)


class Thread(Model):
    class Meta:
        table_name = 'Thread'

    forum_name = UnicodeAttribute(hash_key=True)
    subjects = UnicodeSetAttribute(default=dict)
    views = NumberAttribute(default=0)
    notes = ListAttribute(default=list)


'''
Update Expressions
PynamoDB supports creating update expressions from attributes using a mix of built-in operators and method calls. 
Any value provided will be serialized using the serializer defined for that attribute.
'''

'''
DynamoDB Action / Operator	PynamoDB Syntax	Example
SET	set( value )	Thread.views.set(10)
REMOVE	remove()	Thread.subjects.remove()
ADD	add( value )	Thread.subjects.add({‘A New Subject’, ‘Another New Subject’})
DELETE	delete( value )	Thread.subjects.delete({‘An Old Subject’})
attr_or_value_1 + attr_or_value_2	attr_or_value_1 + attr_or_value_2	Thread.views + 5
attr_or_value_1 - attr_or_value_2	attr_or_value_1 - attr_or_value_2	5 - Thread.views
list_append( attr , value )	append( value )	Thread.notes.append([‘my last note’])
list_append( value , attr )	prepend( value )	Thread.notes.prepend([‘my first note’])
if_not_exists( attr, value )	attr | value	Thread.forum_name | ‘Default Forum Name’
=	==	Thread.forum_name == ‘Some Forum’
<>	!=	Thread.forum_name != ‘Some Forum’
<	<	Thread.views < 10
<=	<=	Thread.views <= 10
>	>	Thread.views > 10
>=	>=	Thread.views >= 10
BETWEEN	between( lower , upper )	Thread.views.between(1, 5)
IN	is_in( *values )	Thread.subject.is_in(‘Subject’, ‘Other Subject’)
attribute_exists ( path )	exists()	Thread.forum_name.exists()
attribute_not_exists ( path )	does_not_exist()	Thread.forum_name.does_not_exist()
attribute_type ( path , type )	is_type()	Thread.forum_name.is_type()
begins_with ( path , substr )	startswith( prefix )	Thread.subject.startswith(‘Example’)
contains ( path , operand )	contains( item )	Thread.subject.contains(‘foobar’)
size ( path)	size( attribute )	size(Thread.subject) == 10
AND	&	(Thread.views > 1) & (Thread.views < 5)
OR	|	(Thread.views < 1) | (Thread.views > 5)
NOT	~	~Thread.subject.contains(‘foobar’)
'''

# Conditional Model.save
# This example saves a Thread item, only if the item exists.
thread_item = Thread('Existing Forum', 'Example Subject')

# DynamoDB will only save the item if forum_name exists
print(thread_item.save(Thread.forum_name.exists()))

# You can specify multiple conditions
print(thread_item.save(Thread.forum_name.exists() & Thread.forum_subject.contains('foobar')))

# Conditional Model.update
# This example will update a Thread item, if the views attribute is less than 5 OR greater than 10:
# thread_item.update(condition=(Thread.views < 5) | (Thread.views > 10))
print(thread_item.delete(Thread.views == 0))

# Conditional Operation Failures
# you can check for conditional operation failures by inspecting the cause of the raised exception:
from pynamodb.exceptions import PutError

try:
    thread_item.save(Thread.forum_name.exists())
except PutError as e:
    if isinstance(e.cause, ClientError):
        code = e.cause.response['Error'].get('Code')
        print(code == "ConditionalCheckFailedException")
