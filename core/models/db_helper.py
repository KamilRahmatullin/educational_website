from asyncio import current_task

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session, AsyncSession

from core.config import settings


class DatabaseHelper:
    """
    A helper class for managing database connections and sessions.
    """

    def __init__(self, url: str, echo: bool = False):
        """
        Initialize the DatabaseHelper with the given database URL and echo mode.

        :param url: The database URL.
        :param echo: If True, SQL statements are printed to the standard error.
        """
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        """
        Get a scoped session for the current task.

        :return: An async scoped session.
        """
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        """
        A dependency for getting a new session for each request.

        :return: An async session.
        """
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        """
        A dependency for getting a scoped session for each request.

        :return: An async session.
        """
        session = self.get_scoped_session()
        yield session
        await session.close()


db_helper = DatabaseHelper(
    url=settings.db.url,
    echo=settings.db.echo,
)
