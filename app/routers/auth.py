from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import Token
from ..models import User
from ..utils import verify_pass
from ..oauth2 import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])

@router.post('/login', response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm =Depends(),db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid username or password')

    pass_check = verify_pass(user_credentials.password, user.password)
    
    if not pass_check:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid username or password')

    #token
    access_token = create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

