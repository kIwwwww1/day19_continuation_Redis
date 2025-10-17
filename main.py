import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, Session
from random_data import FakeData
from json import loads, dumps

engine = create_engine('postgresql://postgres:12345@localhost:5432/postgres')
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
fake = FakeData()

Base = declarative_base()
    
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)

Base.metadata.create_all(engine)

def create_tests_data():

    count = int(input('Сколько данных добавить (число): '))

    try:
        with Session(engine) as session:
            session.add_all([User(name=fake.random_name(), age=fake.randon_age()) for _ in range(count + 1)])
            session.commit()
            print(f'Добавлено {count} пользователей')
    except Exception:
        pass


def create_user():

    name = input('Ваше имя: ')
    age = int(input('Сколько вам лет: '))

    try:
        with Session(engine) as session:
            session.add(User(name=name, age=age))
            session.commit()
            print('Пользователь добавлен')
    except Exception:
            pass
    

def get_all_users():
    cache = redis_client.get('all_users')
    try:
        if cache:
            print(redis_client.get('all_users'), 'Взяли из Redis')
        else:
            with Session(engine) as session:
                users = session.query(User).all()
                ret_users = [f'{i.name} | {i.age}' for i in users]
                redis_client.setex(name='all_users', time=10, value=dumps(ret_users))
                print(redis_client.get('all_users'))
    except Exception:
        pass



def get_user_by_name():
    user_name = input('Введите имя для фильтрации: ')
    user_name = user_name.capitalize()
    try:
        with Session(engine) as session:
            users = session.query(User).filter_by(name=user_name).all()
            for user in users:
                print(f'{user.name}: {user.age}')
    except Exception:
        pass


def menu():
    while True:
        print()
        number = int(input('''Выбeрите пункт меню:
                        
                        1: Добавить тестовые данные
                        2: Добавить пользователя
                        3: Фильтр по имени
                        4: Все пользователи
                           
                        0: Выйти

                        '''))
        
        match number:
            case 1:
                create_tests_data()
            case 2:
                create_user()
            case 3:
                get_user_by_name()
            case 4:
                get_all_users()
            case 0:
                break
            case _:
                pass

menu()