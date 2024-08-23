def clear_posts_from_ads(post, ads_counter):
    for element, value in post.items():
<<<<<<< HEAD
        if element == 'marked_as_ads' and value == 1:
=======
        if element == "marked_as_ads" and value == 1:
>>>>>>> dev
            ads_counter += 1
            del post


def clear_post(post, ads_counter):
<<<<<<< HEAD
    clearing = ['post_source', 'comments', 'reposts', 'is_favorite', 'donut', 'short_text_rate',
                    'can_doubt_category', 'can_set_category', 'signer_id']
    photos_clearing = ['album_id', 'date', 'id', 'owner_id', 'access_key', 'post_id', 'text', 'user_id', 'has_tags']
=======
    clearing = [
        "post_source",
        "comments",
        "reposts",
        "is_favorite",
        "donut",
        "short_text_rate",
        "can_doubt_category",
        "can_set_category",
        "signer_id",
    ]
    photos_clearing = [
        "album_id",
        "date",
        "id",
        "owner_id",
        "access_key",
        "post_id",
        "text",
        "user_id",
        "has_tags",
    ]
>>>>>>> dev

    clear_posts_from_ads(post, ads_counter)
    for post_element in clearing:
        post.pop(post_element, None)
<<<<<<< HEAD
    if 'attachments' in post:
        photo_obj = post['attachments'][0]
        if 'photo' in photo_obj:
            for element in photos_clearing:
                photo_obj['photo'].pop(element, None)
=======
    if "attachments" in post:
        photo_obj = post["attachments"][0]
        if "photo" in photo_obj:
            for element in photos_clearing:
                photo_obj["photo"].pop(element, None)
>>>>>>> dev


def get_cleared_data(data, ads_counter):
    for post in data:
<<<<<<< HEAD
        clear_post(post, ads_counter)
=======
        clear_post(post, ads_counter)
>>>>>>> dev
