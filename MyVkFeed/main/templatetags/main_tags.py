@register.simple_tag(name="countposts")
def count_posts(title: str) -> str:
    count = Post.objects.values("title").filter(title=title).count()
    return f"Постов: {count}"


@register.simple_tag(name="clearerrors")
def clear_filter_errors(context: dict):
    if "errors" in context:
>>>>>>> dev
        context.pop(errors, None)
    else:
        context = None
