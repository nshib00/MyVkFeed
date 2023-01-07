import main.models


def delete_post_duplicates(posts_model: main.models.Post):
    for post in (
        posts_model.objects.values_list("text", flat=True).distinct().iterator()
    ):
        posts_model.objects.filter(
            pk__in=posts_model.objects.filter(text=post).values_list("id", flat=True)[
                1:
            ]
        ).delete()


def delete_image_duplicates(images_model: main.models.Images):
    for image in (
        images_model.objects.values_list("image", flat=True).distinct().iterator()
    ):
        images_model.objects.filter(
            pk__in=images_model.objects.filter(image=image).values_list("id")[1:]
        ).delete()


def delete_group_duplicates(groups_model: main.models.Group):
    for title in (
        groups_model.objects.values_list("group_title", flat=True).distinct().iterator()
    ):
        groups_model.objects.filter(
            pk__in=groups_model.objects.filter(group_title=title).values_list(
                "id", flat=True
            )[1:]
        ).delete()
