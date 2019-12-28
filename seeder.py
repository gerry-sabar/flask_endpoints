from faker import Faker
from db import User

fake = Faker()
for x in range(3):
    User.seed(fake)