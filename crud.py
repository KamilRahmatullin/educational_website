import asyncio

from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User, Profile, Post, Order, Product, OrderProductAssociation


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


async def create_order(session: AsyncSession, promocode: int | None = None) -> Order:
    order = Order(promocode=promocode)
    session.add(order)
    await session.commit()
    return order


async def create_product(session: AsyncSession, name: str, description: str, price: int) -> Product:
    product = Product(name=name, description=description, price=price)
    session.add(product)
    await session.commit()
    return product


async def get_orders_with_products(session: AsyncSession):
    stmt = select(Order).options(
        selectinload(Order.products_details).joinedload(OrderProductAssociation.product)
    ).order_by(Order.id)
    return list(await session.scalars(stmt))


async def create_orders_and_products(session: AsyncSession):
    order_one = await create_order(session)
    order_promo = await create_order(session=session, promocode=15)

    mouse = await create_product(session=session, name="Mouse", description="Great gaming mouse", price=123)
    keyboard = await create_product(session=session, name="Keyboard", description="Great gaming keyboard", price=321)
    display = await create_product(session=session, name="Display", description="Office display", price=299)

    order_one = await session.scalar(
        select(Order).where(Order.id == order_one.id).options(selectinload(Order.products)))
    order_promo = await session.scalar(
        select(Order).where(Order.id == order_promo.id).options(selectinload(Order.products)))

    order_one.products.append(mouse)
    order_one.products.append(keyboard)
    order_promo.products.append(keyboard)
    order_promo.products.append(display)
    order_promo.products.append(mouse)

    await session.commit()


async def demo_get_orders_with_products_through_secondary(session: AsyncSession):
    orders = await get_orders_with_products(session)
    for order in orders:
        print('*' * 10)
        print(order)
        for order_product_details in order.products_details:  # type: OrderProductAssociation
            print('-', order_product_details.product.name, order_product_details.product.price)
        print('*' * 10)
    return orders


async def give_gift_to_order(session: AsyncSession):
    orders = await demo_get_orders_with_products_through_secondary(session)
    gift_product = await create_product(
        session=session,
        name="Gift",
        description="A gift for you",
        price=1000,
    )
    for order in orders:
        order.products_details.append(
            OrderProductAssociation(
                count=1,
                product=gift_product
            )
        )
    await session.commit()


async def main_relations(session: AsyncSession):
    await show_users_with_profiles(session)
    await create_posts(session, 1, 'SQLA 3.0', 'SQLA 3.1', 'SQLA 3.2')
    await get_users_with_posts(session)
    await get_posts_with_authors(session)


async def demo_m2m(session: AsyncSession):
    await demo_get_orders_with_products_through_secondary(session)

    #  await give_gift_to_order(session)


async def main():
    async with db_helper.session_factory() as session:
        await demo_m2m(session)


if __name__ == '__main__':
    asyncio.run(main())
