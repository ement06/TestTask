URL_PREFIRX = "http://127.0.0.1:8000/api/v1/"

class USER_URL:
    SINGUP =  f"{URL_PREFIRX}user/register/"
    LOGIN = f"{URL_PREFIRX}user/login/"
    USER = f"{URL_PREFIRX}user/"


class POST_URL:
    CREATE_OR_GET_POST = f"{URL_PREFIRX}post/"
    RUD_POST = f"{URL_PREFIRX}post/" # Example http://127.0.0.1:8000/api/post/1
    CREATE_OR_GET_LIKE = f"{URL_PREFIRX}post/like/"
    RUD_LIKE = f"{URL_PREFIRX}post/like/", # Example http://127.0.0.1:8000/api/post/like/1
    ANALYST = f"{URL_PREFIRX}post/analyst", # Example http://127.0.0.1:8000/api/post/analyst/?date_from=2020-02-01&date_to=2020-03-01


