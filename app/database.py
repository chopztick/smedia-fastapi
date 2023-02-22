from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = ""
engine = create_engine(f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
tries = 0
while True:
    
    try:
        #password = getpass('Please type password:')
        conn = psycopg.connect(host='localhost', dbname='fastapi', user='babos',
        password='h84tdfdabX', row_factory=dict_row)
        cursor = conn.cursor()
        print('Database connection successful')
        break
    except Exception as error:
        tries +=1
        print('Invalid password, remaining tries: ', 3-tries)
        print('Database connection failed')
        print('Error: ', error)
        if tries == 3:
            sys.exit('Program closed')
        sleep(1)
'''