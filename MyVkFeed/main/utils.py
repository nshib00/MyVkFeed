VERSION = "0.7.0"
YEAR = "2022"

menu = [
    {"title": "Все посты", "url_name": "all_posts"},
    {"title": "Мои подписки", "url_name": "subs"},
    {"title": "Поиск по постам", "url_name": "post_search"},
    {"title": "Фильтры", "url_name": "filters"},
    {"title": "Настройки", "url_name": "settings"},
    {"title": "О сайте", "url_name": "about"},
]


class BaseViewsDataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context["menu"] = menu
        context["version"] = VERSION
        context["year"] = YEAR
        return context