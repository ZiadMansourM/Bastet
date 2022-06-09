from fastapi import APIRouter


router = APIRouter(
    prefix="",
    tags=["main"],
)


@router.get('/')
async def root():
    return {"message": "Hello lets build reusable apps!"}


@router.get('/about')
async def about():
    return {"message": "A project aims to build fastapi using reusable apps (:"}