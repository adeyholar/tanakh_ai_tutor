# src/auth/routes.py - Authentication API Routes
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta

from .models import User, get_db
from .auth_utils import (
    AuthManager, UserAuth, get_current_active_user,
    validate_password_strength, validate_email_format
)

# Create authentication router
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

# Pydantic models for request/response
class UserRegistration(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str  # Can be username or email
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user_info: dict

class UserProfile(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]
    learning_level: str
    total_study_time: int
    words_learned: int
    current_book: str
    current_chapter: int

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

# Authentication Routes
@auth_router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegistration,
    db: Session = Depends(get_db)
):
    """Register a new user account"""
    
    # Validate input data
    if not user_data.username or len(user_data.username.strip()) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be at least 3 characters long"
        )
    
    if not validate_email_format(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    
    if not validate_password_strength(user_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters with letters and numbers"
        )
    
    try:
        # Create user
        new_user = UserAuth.create_user(
            db=db,
            username=user_data.username.strip().lower(),
            email=user_data.email.strip().lower(),
            password=user_data.password,
            full_name=user_data.full_name.strip() if user_data.full_name else None
        )
        
        # Create access token
        access_token = AuthManager.create_access_token(
            data={
                "sub": new_user.username,
                "user_id": new_user.id
            }
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 7 * 24 * 60 * 60,  # 7 days in seconds
            "user_info": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "full_name": new_user.full_name,
                "learning_level": new_user.learning_level
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@auth_router.post("/login", response_model=Token)
async def login_user(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """Authenticate user and return JWT token"""
    
    # Authenticate user
    user = UserAuth.authenticate_user(
        db=db,
        username=user_credentials.username.strip().lower(),
        password=user_credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = AuthManager.create_access_token(
        data={
            "sub": user.username,
            "user_id": user.id
        }
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 7 * 24 * 60 * 60,  # 7 days in seconds
        "user_info": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "learning_level": user.learning_level,
            "total_study_time": user.total_study_time,
            "words_learned": user.words_learned
        }
    }

@auth_router.post("/login/form")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """OAuth2 compatible login endpoint"""
    user = UserAuth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = AuthManager.create_access_token(
        data={"sub": user.username, "user_id": user.id}
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

@auth_router.get("/profile", response_model=UserProfile)
async def get_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user profile information"""
    return UserProfile(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        last_login=current_user.last_login,
        learning_level=current_user.learning_level,
        total_study_time=current_user.total_study_time,
        words_learned=current_user.words_learned,
        current_book=current_user.current_book,
        current_chapter=current_user.current_chapter
    )

@auth_router.put("/profile")
async def update_user_profile(
    full_name: Optional[str] = None,
    learning_level: Optional[str] = None,
    current_book: Optional[str] = None,
    current_chapter: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update user profile information"""
    
    if full_name is not None:
        current_user.full_name = full_name.strip() if full_name.strip() else None
    
    if learning_level in ["beginner", "intermediate", "advanced"]:
        current_user.learning_level = learning_level
    
    if current_book is not None:
        current_user.current_book = current_book
    
    if current_chapter is not None and current_chapter > 0:
        current_user.current_chapter = current_chapter
    
    db.commit()
    
    return {"message": "Profile updated successfully"}

@auth_router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    
    # Verify current password
    if not AuthManager.verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Validate new password
    if not validate_password_strength(password_data.new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be at least 8 characters with letters and numbers"
        )
    
    # Update password
    current_user.hashed_password = AuthManager.hash_password(password_data.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}

@auth_router.post("/logout")
async def logout_user(
    current_user: User = Depends(get_current_active_user)
):
    """Logout user (client should discard token)"""
    return {"message": "Logged out successfully"}

@auth_router.get("/verify-token")
async def verify_token(
    current_user: User = Depends(get_current_active_user)
):
    """Verify if current token is valid"""
    return {
        "valid": True,
        "user_id": current_user.id,
        "username": current_user.username
    }

# Learning progress tracking endpoints
@auth_router.post("/progress/study-time")
async def update_study_time(
    minutes: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update user study time"""
    if minutes > 0:
        current_user.total_study_time += minutes
        db.commit()
    
    return {"message": f"Study time updated (+{minutes} minutes)"}

@auth_router.post("/progress/words-learned")
async def update_words_learned(
    count: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update user words learned count"""
    if count > 0:
        current_user.words_learned += count
        db.commit()
    
    return {"message": f"Words learned updated (+{count} words)"}

@auth_router.get("/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_active_user)
):
    """Get user learning statistics"""
    return {
        "total_study_time": current_user.total_study_time,
        "words_learned": current_user.words_learned,
        "learning_level": current_user.learning_level,
        "current_book": current_user.current_book,
        "current_chapter": current_user.current_chapter,
        "days_since_joined": (datetime.now() - current_user.created_at).days,
        "account_created": current_user.created_at,
        "last_login": current_user.last_login
    }