#from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker
import os
from sqlmodel import SQLModel, create_engine, Session
#import ssl
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

# Get database credentials from environment
username = os.getenv('DB_USERNAME')
password = os.getenv('PASSWORD')
neon_url = os.getenv('NEON_URL')
database = os.getenv('DATABASE')
port = os.getenv('PORT')

if not all([username, password, neon_url, database, port]):
    raise ValueError("Missing one or more environment variables for the database connection.")

# Async database URL (no sslmode in the URL)
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{username}:{password}@{neon_url}/{database}"

# SSL context for asyncpg
#ssl_context = ssl.create_default_context()

# Create async engine with SSL
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    # echo=True,
    # connect_args={"ssl": ssl_context},
)

# Async sessionmaker
# AsyncSessionLocal = sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False
# )

# Base class for ORM models
#Base = declarative_base()

# Dependency for FastAPI routes

def get_db():
    try:
        print("Connecting to DB with:", SQLALCHEMY_DATABASE_URL)
        SQLModel.metadata.create_all(engine)
        print("✅ Tables created")
    except Exception as e:
        print("❌ Error creating tables:", e)

def get_session():
    with Session(engine) as session:
        yield session