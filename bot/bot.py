"Bot for testing TestTask API"

import yaml
import requests
import random
import string

from constants import (
    USER_URL,
    POST_URL,
    PATH_TO_CONFIG
)


def random_string(stringLength: int = 8) -> str:
    """Generate random string for first_name, last_name, email, password, title and body.

    Args:
        stringLength: The first parameter.

    Returns:
        The return random string.

    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def parse_config(path_to_config: str) -> dict:
    """Parse config file.

    Args:
        path_to_config: path to config file.

    Returns:
        Dictionary with `number_of_user`, `max_posts_per_user` and `max_likes_per_user` keys.

    """
    with open(path_to_config) as f:
        return yaml.safe_load(f)


class Bot:
    """Speak with TestTask API."""

    def __init__(self, email, first_name, last_name, password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.header = None

    def register(self):
        """Registers user in TestTask application."""

        requests.post(USER_URL.SINGUP, data={
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password
        })

    def login(self, token: str = None):
        """Authorizes the user in TestTask.

        Args:
            token: token for auth.

        """
        if token is None:
            token = requests.post(USER_URL.LOGIN, data={
                "email": self.email,
                "password": self.password
            }).json()["token"]
        self.header = {'Authorization': f'Bearer {token}'}

    def create_post(self, body: dict) -> int:
        """Creates a post with getting `body`.

        Args:
            body: Contains `title` and `body` of a post.

        Returns:
            Id of a post that was created.

        """
        response = requests.post(POST_URL.CREATE_OR_GET_POST, data=body, headers=self.header)
        return response.json()['id']

    def like_post(self, body):
        """Likes the post with getting `body`.

        Args:
            body: Contains `post_id`.

        """
        requests.post(POST_URL.CREATE_OR_GET_LIKE, data=body, headers=self.header)

    def analyst(self, date_from: str, date_to: str) -> list:
        """Gets likes between `date_from` and `date_to` params.

        Args:
            date_from: date format `2020-02-01`.
            date_to: date format`2020-02-06`.

        Returns:
            Contains a list of likes that stay between the received date.

        """
        response = requests.get(POST_URL.ANALYST, headers=self.header, params={
            'date_from': date_from,
            "date_to": date_to
        })
        return response.json()


class RandomForBot:
    """Creates random users, posts and executes Bot methods."""

    def __init__(self, number_of_user, max_posts_per_user, max_likes_per_user):
        self.number_of_user = number_of_user
        self.max_posts_per_user = max_posts_per_user
        self.max_likes_per_user = max_likes_per_user
        self.random_user = []
        self.random_post = []
        self.all_create_post_ids = []

    def generate_user(self):
        """Generates random users."""

        for i in range(self.number_of_user):
            first_name = random_string()
            user = {
                "first_name": first_name,
                "last_name": random_string(),
                "email": f'{first_name}@gmail.com',
                "password": random_string(16)
            }
            self.random_user.append(user)
        return self.random_user

    def generate_post(self):
        """Generates random posts."""

        for i in range(self.max_posts_per_user * self.number_of_user):
            post = {
                "title": random_string(),
                "body": random_string(20)
            }
            self.random_post.append(post)
        return self.random_post

    def execute(self):
        """Creates instance and performs its methods."""

        for user in self.random_user:
            instance = Bot(**user)
            instance.register()
            instance.login()

            for post in random.choices(self.random_post, k=self.max_posts_per_user):
                self.all_create_post_ids.append(instance.create_post(post))

            for post_id in random.sample(self.all_create_post_ids, k=self.max_likes_per_user):
                instance.like_post({"post_id": post_id})


if __name__ == "__main__":
    values = parse_config(PATH_TO_CONFIG)
    ins = RandomForBot(**values)
    ins.generate_user()
    ins.generate_post()
    ins.execute()
