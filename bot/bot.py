import yaml
import requests
import random
import string
import json

from constants import USER_URL, POST_URL

def random_string(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def parse_config(cls, path_to_config):
    with open(path_to_config) as f:
        return yaml.safe_load(f)
    

class Bot:

    def __init__(self, email, first_name, last_name, password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.header = None

    def register(self):
        response = requests.post(USER_URL.SINGUP, data={
            "email":self.email,
            "first_name":self.first_name,
            "last_name":self.last_name,
            "password": self.password
            })
        return response.status_code == 200
        

    def login(self, token=None):
        if token is None:
            token = requests.post(USER_URL.LOGIN, data={
                "email":self.email,
                "password": self.password
            }).json()["token"]
        self.header = {'Authorization': f'Bearer {token}'}

    def create_post(self, body):
        response = requests.post(POST_URL.CREATE_OR_GET_POST, data=body, headers=self.header)
        return response.json()['id']

    def like_post(self, body):
        response = requests.post(POST_URL.CREATE_OR_GET_LIKE, data=body, headers=self.header)
        return response.status_code == 200
    
    def analyst(self, date_from, date_to):
        response = requests.get(POST_URL.ANALYST, headers=self.header, params={
            'date_from': date_from,
            "date_to": date_to
            })
        return response.json()

class RandomForBot:

    def __init__(self, number_of_user, max_posts_per_user, max_likes_per_user):
        self.number_of_user = number_of_user
        self.max_posts_per_user = max_posts_per_user
        self.max_likes_per_user = max_likes_per_user
        self.random_user = []
        self.random_post = []
        self.all_create_post_ids = []


    def generate_user(self):
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
        for i in range(self.max_posts_per_user*self.number_of_user):
            post = {
                "title": random_string(),
                "body": random_string(20)
            }
            self.random_post.append(post)
        return self.random_post

    def execute(self):
        for user in self.random_user:
            instance = Bot(**user)
            instance.register()
            instance.login()
            for post in range.choice(self.random_post):
                self.all_create_post_ids = instance.create_post(post)
            
            for post_id in self.all_create_post_ids:
                instance.like_post({"post_id": post_id})


if __name__ == "__main__":
    values = parse_config('/home/mishad/python/TestTask/bot/config.yaml')
    ins = RandomForBot(**values)
    print(ins.generate_user())
    print('*****************')
    print(ins.generate_post())
    # a = Bot('test11@gmail.com', 'aaaa', 'bbbb', '123')
    # print(a.login())