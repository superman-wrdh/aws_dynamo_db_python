# Custom Attributes
# https://pynamodb.readthedocs.io/en/latest/attributes.html

# List Attributes
# DynamoDB list attributes are simply lists of other attributes.
# DynamoDB asserts no requirements about the types embedded within the list.
# Creating an untyped list is done like so:
from pynamodb.attributes import ListAttribute, NumberAttribute, UnicodeAttribute, MapAttribute
from pynamodb.models import Model


class GroceryList(Model):
    class Meta:
        table_name = 'GroceryListModel'

    store_name = UnicodeAttribute(hash_key=True)
    groceries = ListAttribute()


# Example usage:

GroceryList(store_name='Haight Street Market',
            groceries=['bread', 1, 'butter', 6, 'milk', 1])

'''
PynamoDB can provide type safety if it is required. Currently PynamoDB does not allow type checks on anything other than MapAttribute and
 subclasses of MapAttribute. We’re working on adding more generic type checking in a future version.
  When defining your model use the of= kwarg and pass in a class. PynamoDB will check that all items in the list are of the type you require.
'''

from pynamodb.attributes import ListAttribute, NumberAttribute


class OfficeEmployeeMap(MapAttribute):
    office_employee_id = NumberAttribute()
    person = UnicodeAttribute()


class Office(Model):
    class Meta:
        table_name = 'OfficeModel'

    office_id = NumberAttribute(hash_key=True)
    employees = ListAttribute(of=OfficeEmployeeMap)


# Example usage:

emp1 = OfficeEmployeeMap(
    office_employee_id=123,
    person='justin'
)
emp2 = OfficeEmployeeMap(
    office_employee_id=125,
    person='lita'
)
emp4 = OfficeEmployeeMap(
    office_employee_id=126,
    person='garrett'
)

Office(
    office_id=3,
    employees=[emp1, emp2, emp4]
).save()  # persists

Office(
    office_id=3,
    employees=['justin', 'lita', 'garrett']
).save()  # raises ValueError

# Map Attributes
'''
DynamoDB map attributes are objects embedded inside of top level models. See the examples here. 
When implementing your own MapAttribute you can simply extend MapAttribute and
 ignore writing serialization code. These attributes can then be used inside of Model classes just like any other attribute.
'''
from pynamodb.attributes import MapAttribute, UnicodeAttribute


class CarInfoMap(MapAttribute):
    make = UnicodeAttribute(null=False)
    model = UnicodeAttribute(null=True)


'''
As with a model and its top-level attributes, a PynamoDB MapAttribute will ignore sub-attributes 
it does not know about during deserialization. As a result, if the item in DynamoDB contains 
sub-attributes not declared as properties of the corresponding MapAttribute, save() will cause those sub-attributes to be deleted.
'''
