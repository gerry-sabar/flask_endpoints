from faker import Faker
from models.user import UserApi

fake = Faker()
for x in range(3):
    UserApi.seed(fake)