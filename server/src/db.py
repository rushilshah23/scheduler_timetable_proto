from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, text



# DATABASE_URL = "sqlite:///my_database.db"  # Using SQLite for this example, replace with PostgreSQL URL in production
DATABASE_URL = "postgresql+psycopg2://postgres:mysecretpassword@172.17.0.3:5432/schedulex"
engine = create_engine(DATABASE_URL, echo=True)
# connection = engine.connect()


Base = declarative_base()




Session = sessionmaker(bind=engine)
session = Session()


# with engine.connect() as conn:
#     result = conn.execute(text("SELECT schedulex();"))
#     print(result.fetchone())