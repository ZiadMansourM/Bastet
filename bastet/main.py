from fastapi import FastAPI

# FIX: Should be registered automatically 
from bastet.store.router import router as store_router
from bastet.core.router import router as core_router


app = FastAPI()


# /
app.include_router(core_router)

# /books
app.include_router(store_router)