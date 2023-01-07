import requests, time, logging

from timeformat import format_time
import config

from handlers import errors_handler, json_handler, photos_handler, posts_handler

logger = logging.getLogger(__name__)


class MyVkFeedLogic:
    data = {}  # все посты записываются сюда
    groups_info = []  # данные о пабликах, на которые подписан пользователь

    def __init__(self, user_id):
        self.user_id = user_id
        self.internet_connection = None

        self.posts_count = 50
        self.ads = 0

        self.group_titles_and_ids = []
        self.posts_photo_refs = []
        self.all_posts_photo_counter = [0] * (
            self.posts_count + 1
        )  # счётчик фото в каждом из постов. Индекс списка - номер поста.

    def load_posts_from_vk(self):
        self.groups_req = requests.get(
            f"https://api.vk.com/method/groups.get?access_token={config.VK_API_TOKEN}&user_id={self.user_id}&extended=1&v=5.131"
        )
        self.feed_req = requests.get(
            f"https://api.vk.com/method/newsfeed.get?&access_token={config.VK_API_TOKEN}&filters=post&count={self.posts_count}&v=5.131"
        )
        errors_handler.check_vk_api_errors(self)
        self.data = self.feed_req.json()["response"]["items"]
        json_handler.save_posts_to_json(posts=self.data)

    def get_post_author_nickname(self):
        pass

    def get_post_title(self, post_object):
        self.get_group_titles_and_ids()
        for post_title, post_id in self.group_titles_and_ids:
            source_id = int(str(post_object[0]["source_id"]).replace("-", ""))
            # if post_title is None:
            #     post_title = self.get_post_author_nickname()
            if source_id == int(post_id):
                return post_title

    def get_groups_info(self):
        if self.internet_connection:
            for item in self.groups_req.json()["response"]["items"]:
                self.groups_info.append(
                    {
                        "title": item["name"],
                        "domain": item["screen_name"],
                        "id": str(item["id"]),
                        "photo": item["photo_50"],
                    }
                )
        # названия групп не отображаются в оффлайн-режиме!

    def get_group_titles_and_ids(self):
        for item in self.groups_info:
            self.group_titles_and_ids.append((item["title"], item["id"]))

    def get_posts_text(self):
        return [post for post in self.data]

    def get_posts_photo_refs(self):
        for index, post in enumerate(self.data):
            if "attachments" in post:
                post_photos = [
                    item for item in post["attachments"] if item["type"] == "photo"
                ]
                photos_handler.get_filtered_post_photos(
                    photo_list=post_photos,
                    photo_counter=self.all_posts_photo_counter,
                    post_number=index,
                    final_photo_refs_list=self.posts_photo_refs,
                )
                # for item in all_post_photos:
                # if item['type'] == 'link' and 'photo' in item:
                #     refs = logic.photos_filter.filter_photos_by_size(item['link']['photo']['sizes'])
                # elif item['type'] == 'photo':
            if "copy_history" in post:
                for item in post["copy_history"]:
                    if "attachments" in item:
                        post_photos = [
                            attachment
                            for attachment in item["attachments"]
                            if attachment["type"] == "photo"
                        ]
                        photos_handler.get_filtered_post_photos(
                            photo_list=post_photos,
                            photo_counter=self.all_posts_photo_counter,
                            post_number=index,
                            final_photo_refs_list=self.posts_photo_refs,
                        )

    def get_posts_text_with_refs(self):
        posts_text_with_refs = list(zip(self.get_posts_text(), self.posts_photo_refs))
        self.posts_count = len(posts_text_with_refs)
        return posts_text_with_refs

    def get_post(self, post_index):
        post = self.posts_text_with_refs[post_index]
        if not post[0].get("text") or post[0].get("text").startswith("#"):
            post[0]["text"] = ""
        formatted_time = str(time.ctime(post[0]["date"])[4:])
        post_dict = {
            "date": format_time(formatted_time),
            "title": self.get_post_title(post),
            "text": post[0]["text"],
            "photo_ref": str(post[1]),
            "accurate_date": post[0]["date"],
            "photo_count": self.all_posts_photo_counter[post_index],
        }
        if not post[1]:
            post_dict["photo_ref"] = "<no_images>"
            post_dict["photo_count"] = 0
        return post_dict

    def load_data(self):
        if self.user_id is not None:
            try:
                posts_handler.get_cleared_data(data=self.data, ads_counter=self.ads)
                self.load_posts_from_vk()
                self.get_groups_info()
                self.get_posts_photo_refs()
                self.get_group_titles_and_ids()
                self.posts_text_with_refs = self.get_posts_text_with_refs()
            except Exception as err:
                logger.error(f"Ошибка: {err}")
            except requests.exceptions.ConnectionError:
                self.internet_connection = False
                logger.warning("Нет подключения к интернету.")
            else:
                self.internet_connection = True
                logger.info(
                    f"Код запроса к группам: {self.groups_req.status_code}, код запроса к стене: {self.feed_req.status_code}."
                )
                logger.info(
                    f"Загружено постов: {len(self.data)}, удалено рекламных постов: {self.ads}."
                )
            finally:
                self.ads = 0
        if not self.internet_connection:
            json_handler.load_posts_from_json()
            logger.info("Работает оффлайн-режим приложения.")
