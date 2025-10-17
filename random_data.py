from faker import Faker
from random import randint

class FakeData:
    def __init__(self) -> None:
        self.fake = Faker('ru_RU')
    
    def random_name(self):
        return self.fake.first_name()
    
    def randon_age(self):
        return randint(1, 100)