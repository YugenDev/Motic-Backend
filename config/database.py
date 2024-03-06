import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlite_database = "database.sqlite"
base_dir = os.path.dirname(os.path.realpath(__file__))


database_url = "mysql+pymysql://root:@localhost:3306/motic"

engine = create_engine(database_url, echo=True)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)
