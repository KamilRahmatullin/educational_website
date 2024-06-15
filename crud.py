import asyncio

from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User, Profile, Post


async def create_user(session: AsyncSession, username: str):
    """
    This function creates a new user in the database.
    """
    user = User(username=username)  # Create a new User object
    session.add(user)  # Add the User object to the session
    await session.commit()  # Commit the changes to the database
    return user  # Return the newly created User object


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    """
    This function retrieves a user from the database based on their username.
    """
    stmt = select(User).where(User.username == username)
    user: User | None = await session.scalar(stmt)
    return user


async def create_user_profile(session: AsyncSession, user_id: int, first_username: str | None = None,
                              last_username: str | None = None) -> Profile:
    profile = Profile(user_id=user_id, first_username=first_username, last_username=last_username)
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession) -> list[User]:
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile.first_username)


async def create_posts(session: AsyncSession, user_id: int, *posts_titles: str) -> list[Post]:
    posts = [
        Post(user_id=user_id, title=post_title)
        for post_title in posts_titles
    ]
    session.add_all(posts)
    await session.commit()
    return posts


async def get_users_with_posts(session: AsyncSession):
    """
    This function retrieves users from the database along with their associated posts.

    Note:
    This function uses selectinload to eagerly load the 'posts' relationship for each user.
    It executes the query twice to fetch the users and their posts separately.
    The first fetch is done using session.execute to get the Result object,
    and the second fetch is done using session.scalars to get the User objects.
    """

    # Create a SQLAlchemy select statement for User, with selectinload for 'posts' relationship
    stmt = select(User).options(
        selectinload(User.posts)).order_by(User.id)  # many posts to one user

    # Execute the SQL statement and get the Result object
    result: Result = await session.execute(stmt)

    # Fetch the User objects from the Result object
    users = result.scalars()

    # Fetch the User objects again, this time with their associated posts
    users = await session.scalars(stmt)

    # Iterate over the users and their associated posts
    for user in users:
        for post in user.posts:
            print(post)


async def get_posts_with_authors(session: AsyncSession):
    stmt = select(Post).options(
        joinedload(Post.user)).order_by(Post.id)  # one user to many posts
    posts = await session.scalars(stmt)
    return posts


async def main_relations(session: AsyncSession):
    await show_users_with_profiles(session)
    await create_posts(session, 1, 'SQLA 3.0', 'SQLA 3.1', 'SQLA 3.2')
    await get_users_with_posts(session)
    await get_posts_with_authors(session)


async def demo_m2m(session: AsyncSession):
    pass


async def main():
    async with db_helper.session_factory() as session:
        await demo_m2m(session)


if __name__ == '__main__':
    asyncio.run(main())
