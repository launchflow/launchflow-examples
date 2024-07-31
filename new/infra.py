import launchflow as lf
import asyncio
import launchflow as lf
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from contextlib import asynccontextmanager
from app.logger import logger
import app.types.acats_fields as types


vm = lf.gcp.ComputeEnginePostgres("recommendation-api-vm")

if __name__ == "__main__":
    print(vm.outputs())
