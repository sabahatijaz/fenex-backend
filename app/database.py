import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from databases import Database as AsyncDatabase

# Load environment variables from .env
load_dotenv()

# Create a base class for models
Base = declarative_base()

# Singleton class to handle database connections
class DatabaseHandler:
    __instance = None
    db = None

    @staticmethod
    def getInstance():
        """
        Static access method to get the singleton instance.
        """
        if DatabaseHandler.__instance is None:
            DatabaseHandler()
        return DatabaseHandler.__instance

    def __init__(self):
        """
        Virtually private constructor to create the singleton instance.
        Initializes the database connection settings.
        """
        if DatabaseHandler.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DatabaseHandler.__instance = self

            # Load database credentials from environment variables
            DB_USER = os.getenv("DB_USERNAME")
            DB_PASSWORD = os.getenv("DB_PASSWORD")
            DB_HOST = os.getenv("DB_HOSTNAME")
            DB_PORT = os.getenv("DB_PORT")
            DB_NAME = os.getenv("DB_NAME")

            # Construct the database URL for async PostgreSQL connection
            self.url = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

            # Initialize the async database object for raw queries
            self.db = AsyncDatabase(self.url)

            # Initialize the async SQLAlchemy engine and session factory
            self.engine = create_async_engine(self.url, echo=False)
            self.async_session = sessionmaker(
                bind=self.engine,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False,
                class_=AsyncSession
            )

    async def init_db(self):
        """
        Initializes the database by creating all tables.
        This should be called once at the start of the application.
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


# Wrapper class for database interactions
class Database:
    """
    A class for managing database connections and operations.
    """

    def __init__(self):
        """
        Initializes the Database instance by acquiring a singleton instance of DatabaseHandler.
        """
        tmp = DatabaseHandler.getInstance()
        self.db = tmp.db
        self.async_session = tmp.async_session

    async def connect(self):
        """
        Connect to the database.
        """
        await self.db.connect()

    async def disconnect(self):
        """
        Disconnect from the database.
        """
        await self.db.disconnect()

    async def init_db(self):
        """
        Initialize the database by calling the DatabaseHandler's init_db method.
        This ensures the tables are created based on the models.
        """
        await DatabaseHandler.getInstance().init_db()

    async def log(self, action, execution_time_ms, data):
        """
        Log database actions for tracking and debugging.
        """
        async with self.async_session() as session:
            new_log_item = models.FunctionCallLog(
                action=action,
                execution_time_ms=execution_time_ms,
                data=data,
            )
            session.add(new_log_item)
            await session.commit()
