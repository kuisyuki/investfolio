from application.use_cases.register_user import RegisterUserUseCase
from application.use_cases.login_user import LoginUserUseCase
from fastapi import APIRouter, Depends, HTTPException, status
from infrastructure.database import get_db
from infrastructure.repositories.user_repository import SQLUserRepository
from infrastructure.jwt_utils import create_access_token
from sqlalchemy.orm import Session

from presentation.dependencies.auth import get_current_user
from presentation.schemas.auth import (
    LoginRequest,
    LoginResponse,
    UserCreateRequest,
    UserResponse,
)
from domain.entities.auth import User

router = APIRouter(prefix="/api/auth")


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"],
)
async def register_user(request: UserCreateRequest, db: Session = Depends(get_db)):
    """テスト用のユーザー登録エンドポイント"""
    try:
        # リポジトリとユースケースの初期化
        user_repository = SQLUserRepository(db)
        use_case = RegisterUserUseCase(user_repository)

        # ユーザーを登録
        user = await use_case.execute(
            username=request.username,
            email=request.email,
            password=request.password,
            full_name=request.full_name,
        )

        # レスポンスに変換
        return UserResponse(
            id=user.id,
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    tags=["Authentication"],
)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """ユーザーログインエンドポイント"""
    try:
        # リポジトリとユースケースの初期化
        user_repository = SQLUserRepository(db)
        use_case = LoginUserUseCase(user_repository)

        # ユーザー認証
        user = await use_case.execute(email=request.email, password=request.password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # アクセストークンを生成
        access_token = create_access_token(data={"sub": str(user.id)})

        # レスポンスを作成
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse(
                id=user.id,
                user_id=user.user_id,
                username=user.username,
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active,
                is_verified=user.is_verified,
                created_at=user.created_at,
                updated_at=user.updated_at,
            ),
        )

    except HTTPException:
        raise
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    tags=["Authentication"],
)
async def get_me(current_user: User = Depends(get_current_user)):
    """現在のユーザー情報を取得するエンドポイント"""
    return UserResponse(
        id=current_user.id,
        user_id=current_user.user_id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )


@router.get("/test", tags=["Test"])
async def test_auth():
    """認証APIの動作確認用エンドポイント"""
    return {"message": "Auth API is working"}
