from fastapi.testclient import TestClient

from app.test.test_init import app
from app.schemas.users import Token



client = TestClient(app)
client.base_url += "/api/"


def test_get_post_list():
    response = client.get("post")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "nickname": "테스트",
            "title": None,
            "like_count": 0,
            "bucketlist": [],
            "updated_at": None
        }
    ]


def test_get_post_detail_success():
    response = client.get("post/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "nickname": "테스트",
        "owner": False,
        "bookmark": False,
        "like": False,
        "like_count": 0,
        "title": None,
        "updated_at": None,
        "bucketlist": []
    }


def test_create_bucketlist_success():
    response = client.put(
        "bucketlist",
        headers={
            "Authorization": "Bearer"
        },
        json={
            "title": "테스트의 버킷리스트",
            "bucketlist": [
                {
                    "content": "서핑하기",
                    "date": "2022-06-20",
                    "image_path": "images/image1.jpg"
                },
                {
                    "content": "미국 여행가기"
                },
            ]
        }
    )
    assert response.status_code == 204


def test_create_bucketlist_failure():
    response = client.put(
        "bucketlist",
        json={
            "title": "테스트의 버킷리스트",
            "bucketlist": [
                {
                    "content": "서핑하기",
                    "date": "2022-06-20",
                    "image_path": "images/image1.jpg"
                },
                {
                    "content": "미국 여행가기"
                },
            ]
        }
    )
    assert response.status_code == 401


def test_update_bucketlist_success():
    response = client.put(
        "bucketlist",
        headers={
            "Authorization": "Bearer"
        },
        json={
            "title": "테스트의 버킷리스트",
            "bucketlist": [
                {
                    "id": 1,
                    "content": "서핑하기",
                    "date": "2023-06-20",
                    "image_path": "images/image1.jpg"
                },
                {
                    "content": "한라산 등산하기"
                },
            ]
        }
    )
    assert response.status_code == 204


def test_delete_bucketlist_success():
    response = client.delete(
        "bucketlist/1",
        headers={
            "Authorization": "Bearer"
        }
    )
    assert response.status_code == 204


def test_delete_bucketlist_failure_1():
    response = client.delete(
        "bucketlist/2",
    )
    assert response.status_code == 401


def test_delete_bucketlist_failure_2():
    response = client.delete(
        "bucketlist/100",
        headers={
            "Authorization": "Bearer"
        }
    )
    assert response.status_code == 404
