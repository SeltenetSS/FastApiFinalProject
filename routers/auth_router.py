# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# import crud, schemas
# from database import get_db
# from auth import verify_password, create_access_token
#
# router = APIRouter(prefix="/api/auth", tags=["Auth"])
#
# @router.post("/register", response_model=schemas.UserOut)
# def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     try:
#         db_user = crud.get_user_by_email(db, user.email)
#         if db_user:
#             raise HTTPException(status_code=400, detail="Email already registered")
#         return crud.create_user(db, user)
#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail="Internal server error")
#
# @router.post("/login", response_model=schemas.Token)
# def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, user.email)
#     if not db_user or not verify_password(user.password, db_user.hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     token = create_access_token({"sub": db_user.email})
#     return {"access_token": token, "token_type": "bearer"}
#
#

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db
from auth import verify_password, create_access_token, SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi import Security
router = APIRouter(prefix="/api/auth", tags=["Auth"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = crud.get_user_by_email(db, email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = crud.get_user_by_email(db, user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return crud.create_user(db, user)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")



@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "full_name": db_user.full_name,
            "email": db_user.email,
            "is_admin": db_user.is_admin
        }
    }





@router.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user: schemas.UserOut = Security(get_current_user)):
    return current_user