from fastapi import APIRouter, status, Depends, HTTPException
import models
import auth


router = APIRouter(
    prefix="/users",
    tags=["Authentication and Authorization"],
)

auth_handler = auth.AuthHandler()
users = []


@router.post('/register', status_code=status.HTTP_201_CREATED)
def register(auth_details: models.AuthDetails):
    if any(x['username'] == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append({
        'username': auth_details.username,
        'password': hashed_password    
    })
    return



@router.post('/login')
def login(auth_details: models.AuthDetails):
    user = next((x for x in users if x['username'] == auth_details.username), None)
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return { 'token': token }


@router.get('/unprotected')
def unprotected():
    return {'message': 'Hello world!'}


@router.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    return { 'name': username }
