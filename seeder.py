import click
from flask import Flask

app = Flask(__name__)
@app.cli.command("seeder")

def seed():
    from faker import Faker
    from models.user import UserApi

    fake = Faker()
    for x in range(3):
        UserApi.seed(fake)