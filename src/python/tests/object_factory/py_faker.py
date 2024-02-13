from faker import Faker
from faker.providers import python

PY_FAKER = Faker()
PY_FAKER.add_provider(python)
