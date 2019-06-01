from faker import Faker

f = Faker(locale='en_US')

for i in range(100):
    print(f.name())
