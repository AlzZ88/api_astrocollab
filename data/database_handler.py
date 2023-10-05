from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Define the database URL, you can change this according to your database
#DATABASE_URL = "postgresql://username:password@localhost:5432/astrocollab"

#CREDENTIALS
""" USER="asanchez2017""servicio_movil"
PASSWORD="153alex531""astrocollab888"
HOST="localhost:3306" """

USER="asanchez2017"
PASSWORD="153alex531"

HOST = "localhost"
PORT = "5432"
DATABASE="astrocollab"


DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

print(DATABASE_URL)

#DATABASE_URL = "sqlite:///./db/astrocollab.db"

# Create a SQLAlchemy database engine
engine = create_engine(DATABASE_URL)


# Create a sessionmaker with specific settings
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a base class for declarative models
Base = declarative_base()

def get_db():
    """
    Get a database session.

    Returns:
        generator: A generator that yields a database session.
    """
    """db = SessionLocal()
    print("[INFO] Connecting with Astrollab...")
    try:
        yield db
    except BaseException as e:
        print(f"[ERROR] an error occurred while trying to connect to astrocollab: {e}")
    finally:
        db.close()"""

    """
    Get a database session.

    Returns:
        generator: A generator that yields a database session.
    """
    db = SessionLocal()
    print("[INFO] Connecting with Astrollab...")
    try:
        yield db
    except Exception as e:
        db.rollback()  # Rollback any changes made in the session
        print(f"[ERROR] An error occurred while trying to connect to astrocollab: {e}")
        raise  # Re-raise the exception to propagate it further
    finally:
        db.close()

def create_tables():
    """
    Create database tables.

    This function creates tables based on the SQLAlchemy models.
    """
    print("[INFO] Creating tables...")

    try:
        Base.metadata.create_all(bind=engine)
    except BaseException as e:
        print(f"[ERROR] an error occurred while trying to create database : {e}")
