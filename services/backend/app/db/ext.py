from app.db.database import session_factory

def connection(method):
    """
    Decorator for transaction processing
    """
    async def wrapper(*args, **kwargs):
        async with session_factory() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper
