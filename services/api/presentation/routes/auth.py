from application.use_cases.register_user import RegisterUserUseCase
from fastapi import APIRouter, Depends, HTTPException, status
from infrastructure.database import get_db
from infrastructure.repositories.user_repository import SQLUserRepository
from sqlalchemy.orm import Session

from presentation.schemas.auth import UserCreateRequest, UserResponse

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


@router.get("/test", tags=["Test"])
async def test_auth():
    """認証APIの動作確認用エンドポイント"""
    return {"message": "Auth API is working"}
