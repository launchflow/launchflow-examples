import launchflow as lf

# Create the global FastAPI dependency for the SQLAlchemy async session
async_session = lf.fastapi.sqlalchemy_async_depends()
