from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException, 
    Body,
    Response,
    Cookie
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_db,
    get_current_user
)
from app.schemas.users import User, UserCreate, Token, UserLogin, UserWithPostId, PostId
from app.schemas.common import HTTPError
from app.crud.users import (
    create_user, 
    get_user, 
    get_user_by_nickname,
    get_user_by_id,
    update_user_nickname,
    update_user_password,
    update_user_profile,
    delete_user
)
from app.crud.posts import create_post
from app.core.config import settings
from app.core.security import (
    create_token, 
    get_kakao_token, 
    get_kakao_user_email,
    verify_password,
    decode_token
)
from app.utils import send_email_code, generate_random_password, send_new_password



router = APIRouter()


@router.post("/email", status_code=204, responses={400: {}}, summary="이메일 중복확인 및 인증메일 전송", tags=["유저"])
def check_email(response: Response, email: str = Body(..., embed=True), db: Session = Depends(get_db)):
    if get_user(db, email):
        raise HTTPException(status_code=400)
    try:
        code = send_email_code(email)
        response.set_cookie(key="email_code", value=code, max_age=600, httponly=True)
    except:
        raise HTTPException(status_code=400)
    return


@router.post("/email/code", status_code=204, responses={400: {}}, summary="이메일 인증코드 확인", tags=["유저"])
def check_email_code(response: Response, code: str = Body(..., embed=True), email_code: str | None = Cookie(None)):
    """
    **Cookie**
    - email_code: 이메일로 보내진 인증코드가 담겨져 있는 쿠키로 서버에서 인증 메일을 보낼 때 set-cookie함.

    **Body**
    - code: 사용자가 입력한 인증코드
    """
    if code and email_code and code == email_code:
        response.delete_cookie("email_code")
        return
    raise HTTPException(status_code=400)


@router.post("/nickname", status_code=204, responses={400: {}}, summary="닉네임 중복확인", tags=["유저"])
def check_nickname(nickname: str = Body(..., embed=True), db: Session = Depends(get_db)):
    if get_user_by_nickname(db, nickname):
        raise HTTPException(status_code=400)
    return


@router.post("/signup", status_code=201, response_class=Response, responses={400: {}}, summary="회원가입", tags=["유저"])
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if get_user(db, user.email):
        raise HTTPException(status_code=400)
    if get_user_by_nickname(db, user.nickname):
        raise HTTPException(status_code=400)
    user = create_user(db, user)
    create_post(db, user.id)
    return


@router.post(
    "/login", 
    response_model=Token, 
    responses={
        400: {
            "model": HTTPError,
            "content": {
                "application/json": {
                    "examples": {
                        "이메일이 틀렸을 때": {
                            "value": {
                                "detail": "email"
                            }
                        },
                        "비밀번호가 틀렸을 때": {
                            "value": {
                                "detail": "password"
                            }
                        }
                    }
                }
            }
        }
    },
    summary="로그인",
    tags=["유저"]
)
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    **Body**
    - username: 이메일
    - password: 비밀번호
    """
    user = get_user(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="email",
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="password",
        )
    token = create_token(user.email)
    refresh_token = token.pop("refresh_token")
    response.set_cookie("refresh_token", refresh_token, max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES*60)
    return token


@router.get("/refresh", response_model=Token, responses={400: {}}, summary="토큰 갱신", tags=["유저"])
def refresh_token(response: Response, refresh_token: str | None = Cookie(None), db: Session = Depends(get_db)):
    print(f"refresh token: {refresh_token}")
    email = decode_token(refresh_token)
    user = get_user(db, email)
    if user is None:
        raise HTTPException(status_code=400)
    token = create_token(user.email)
    refresh_token = token.pop("refresh_token")
    response.set_cookie("refresh_token", refresh_token, max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES*60)
    return token


@router.get("/logout", status_code=204, summary="로그아웃", tags=["유저"])
def logout(response: Response):
    response.delete_cookie("refresh_token")
    return


@router.get("/me", response_model=UserWithPostId, responses={401: {}}, summary="현재 유저 정보 조회", tags=["유저"])
def get_current_user_info(user: User = Depends(get_current_user)):
    user.post_id = user.post.id
    return user


@router.get("/user/{user_id}/post", response_model=PostId, responses={404: {}}, summary="유저의 게시글 아이디 및 공개여부 조회", tags=["유저"])
def get_post_id(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404)
    return user.post


@router.patch("/nickname", status_code=204, responses={400: {}, 401: {}}, summary="닉네임 수정", tags=["마이페이지"])
def update_nickname(nickname: str = Body(..., embed=True), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    nickname = nickname.strip()
    if not nickname:
        raise HTTPException(status_code=400)
    update_user_nickname(db, user.id, nickname)
    return


@router.patch("/password", status_code=204, responses={400: {}, 401: {}, 403: {}}, summary="비밀번호 수정", tags=["마이페이지"])
def update_password(password: str = Body(..., embed=True), new_password: str = Body(..., embed=True), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(password, user.password):
        raise HTTPException(status_code=403)
    new_password = new_password.strip()
    if len(new_password) < 8:
        raise HTTPException(status_code=400)
    update_user_password(db, user.id, new_password)
    return


@router.post("/password", status_code=204, responses={401: {}}, summary="비밀번호 찾기", tags=["마이페이지"])
def find_password(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_password = generate_random_password()
    update_user_password(db, user.id, new_password)
    send_new_password(user.email, new_password)
    return


@router.get("/profile/presigned-post", summary="S3에 프로필 이미지 업로드를 위한 Presigned POST 요청", tags=["마이페이지"])
def get_presigned_post(file_name: str, user: User = Depends(get_current_user)):
    file_type = file_name.split(".")[-1]
    response = requests.post(
        f"{settings.AWS_API_GATEWAY_URL}/presigned-post",
        headers={"Authorization": settings.AWS_AUTH_KEY},
        json={"type": "profile", "name": f"profile.{file_type}", "id": user.id}
    ).json()
    if response.get("error"):
        return response.get("message")
    return response.get("data")


@router.patch("/profile", status_code=204, responses={401: {}}, summary="프로필 사진 경로 수정", tags=["마이페이지"])
def update_profile(image_path: str | None = Body(None, embed=True), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not image_path:
        image_path = None
    update_user_profile(db, user.id, image_path)
    return


@router.delete("/user", status_code=204, responses={401: {}, 403: {}}, summary="회원 탈퇴", tags=["마이페이지"])
def delete_user_info(password: str = Body(..., embed=True), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(password, user.password):
        raise HTTPException(status_code=403)
    delete_user(db, user.id)
    return


# @router.post("/token/kakao", response_model=Token)
# def kakao_login(code: str = Body(...)):
#     response = get_kakao_token(code)
#     data = response.json()
#     if response.status_code != 200:
#         raise HTTPException(status_code=400)
#     response = get_kakao_user_email(data.get("access_token"))
#     data = response.json()
#     if response.status_code != 200:
#         raise HTTPException(status_code=400)
#     print("========================response")
#     print(data)
#     print(response.status_code)
#     return 

