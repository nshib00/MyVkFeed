from allauth.socialaccount.models import SocialAccount
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q

from endless_pagination.views import AjaxListView

import logging

from logic.main_logic import MyVkFeedLogic
import logic.db

from .utils import *
from .forms import *

logger = logging.getLogger(__name__)


class MainPage(BaseViewsDataMixin, AjaxListView):
    ''' Главная страница приложения. '''
    model = Post
    context_object_name = 'posts'
    paginate_by = 3
    posts_count = Post.objects.count()

    def load_logic(self):
        request_user_id = self.request.user.pk
        if request_user_id is None:
            self.logic_obj = MyVkFeedLogic(user_id=None)
        else:
            current_user_id = int(
                                    SocialAccount.objects.filter(user_id=request_user_id).values_list('uid')[0][0]
                                 )
            self.logic_obj = MyVkFeedLogic(user_id=current_user_id)
            self.logic_obj.load_data()

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return r'account\login.html'
        else:
            return r'main\start_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.object_list
        context['user'] = self.request.user
        self.load_logic()
        self.load_and_save_data()
        basecontext = self.get_user_context(
            title='MyVkFeed',
            posts_count=self.logic_obj.posts_count,
            # images=[]
            # images=Images.objects.select_related('post').all()
        )
        return dict(list(context.items()) + list(basecontext.items()))

    def load_and_save_groups(self):
        for group in self.logic_obj.groups_info:
            Group.objects.update_or_create(group_title=group['title'], image=group['photo'])

    def load_and_save_data(self):
        if self.logic_obj.user_id is not None:
            logic.db.delete_post_duplicates(posts_model=Post)
            logic.db.delete_image_duplicates(images_model=Images)
            logic.db.delete_group_duplicates(groups_model=Group)
            self.load_and_save_groups()
            for index in range(len(self.logic_obj.posts_text_with_refs)):
                post = self.logic_obj.get_post(post_index=index)
                if post['title'] is not None:
                    by_hidden_group = Group.objects.get(group_title=post['title']).is_hidden
                                                     # .filter(group_title=post['title']).values().first()['is_hidden']
                else:
                    by_hidden_group = 0
                if by_hidden_group:
                    saved_post_obj = Post.objects.get(date=post['date'], title=post['title'])
                    saved_post_obj.update(by_hidden_group=by_hidden_group)
                else:
                    saved_post_obj = Post.objects.update_or_create(
                            date=post['date'],
                            title=post['title'],
                            text=post['text'],
                            accurate_date=post['accurate_date'],
                            photo_count=post['photo_count'],
                            by_hidden_group=by_hidden_group,
                    )
                    post_obj = saved_post_obj[0]
                    post_images = []
                    for ref in post['photo_ref'].split('\n'):
                        image_obj = Images.objects.update_or_create(post=post_obj, image=ref)
                        post_images.append(image_obj[0])
                    post_obj.photos.add(*post_images)


    def get_queryset(self):
        if self.posts_count >= 50:
            return Post.objects.filter(by_hidden_group=0)[:51]
        else:
            return Post.objects.filter(by_hidden_group=0)


class PostView(BaseViewsDataMixin, DetailView):
    ''' Отображение поста под номером postid. '''
    model = Post
    template_name = 'main/post.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        postid = kwargs["object"].pk
        context = super().get_context_data(**kwargs)
        basecontext = self.get_user_context(title=f'MyVkFeed | Пост #{postid}')
        return dict(list(context.items()) + list(basecontext.items()))


class SubsView(BaseViewsDataMixin, ListView):
    model = Group
    template_name = 'main/subs.html'
    context_object_name = 'groups'
    groups_count = 0

    def get_queryset(self):
        query = self.request.GET.get('group_title')
        if query is not None:
            filtered_groups = Group.objects.filter(is_hidden=False, group_title__icontains=query)
            self.groups_count = len(filtered_groups)
            return filtered_groups
        else:
            return Group.objects.filter(is_hidden=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SubsSearchForm()
        context['groups_count'] = self.groups_count
        basecontext = self.get_user_context(title='Mои подписки')
        return dict(list(context.items()) + list(basecontext.items()))


class PostSearchView(BaseViewsDataMixin, ListView):
    model = Post
    template_name = 'main/post_search.html'
    context_object_name = 'posts'

    def __init__(self):
        super().__init__()
        self.posts_count = 0

    def get_queryset(self):
        query = self.request.GET.get('text')
        if query is not None:
            searched_posts = Post.objects.filter(Q(text__icontains=query) | Q(title__icontains=query))
        else:
            searched_posts = Post.objects.all()
        self.posts_count = searched_posts.count()
        return searched_posts


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts_count'] = self.posts_count
        basecontext = self.get_user_context(title='Поиск по постам')
        context['form'] = PostSearchForm()
        return dict(list(context.items()) + list(basecontext.items()))


class FiltersView(BaseViewsDataMixin, ListView):
    template_name = 'main/filters.html'
    model = Group
    queryset = Group.objects.all()
    form_context = {}
    context_object_name = 'groups'

    @staticmethod
    def format_groups_list(groups_list):
        if len(groups_list) == 1:
            return groups_list[0]
        elif 2 <= len(groups_list) <= 5:
            return ', '.join(groups_list)
        else:
            return ', '.join(groups_list[:6])

    def format_filter_message(self, groups_list, context_dict, action=None):
        groups = self.format_groups_list(groups_list)
        if action == 'hide':
            if len(groups_list) == 1:
                context_dict['filter_message'] = f'Группа {groups} была скрыта из ленты.'
            elif 2 <= len(groups_list) <= 5:
                context_dict['filter_message'] = f'Группы {groups} были скрыты из ленты.'
            else:
                context_dict['filter_message'] = f'{groups} и еще {len(groups_list)-5} групп были скрыты из ленты.'
        elif action == 'show':
            if len(groups_list) == 1:
                context_dict['filter_message'] = f'Посты группы {groups} вновь отображаются в ленте.'
            elif 2 <= len(groups_list) <= 5:
                context_dict['filter_message'] = f'Посты групп {groups} вновь отображаются в ленте.'
            else:
                context_dict['filter_message'] = f'Посты {groups} и {len(groups_list)-5} других групп вновь отображаются в ленте.'

    def post(self, request):
        form = FiltersForm(request.POST)
        request_list = list(request.POST.lists())
        try:
            groups = request_list[1][1]
        except IndexError as error:
            self.form_context['errors'] = error
        else:
            for group in groups:
                if request_list[1][0] == 'groups-to-hide-select[]':
                    Group.objects.filter(group_title=group, is_hidden=0).update(is_hidden=1)
                    self.format_filter_message(groups, self.form_context, action='hide')
                elif request_list[1][0] == 'groups-to-show-select[]':
                    Group.objects.filter(group_title=group, is_hidden=1).update(is_hidden=0)
                    self.format_filter_message(groups, self.form_context, action='show')
            self.form_context['form'] = form
        return HttpResponseRedirect('/filters/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        basecontext = self.get_user_context(title='Фильтры')
        return dict(list(self.form_context.items()) + list(context.items()) + list(basecontext.items()))


class GroupView(BaseViewsDataMixin, DetailView):
    template_name = 'main\group.html'
    model = Group
    context_object_name = 'group'

    def get_context_data(self, *, object_list=None, **kwargs):
        showing_group_title = kwargs["object"].group_title
        context = super().get_context_data(**kwargs)
        context['posts_handlers'] = Post.objects.filter(title=showing_group_title)
        context['posts_count'] = context['posts_handlers'].count()
        basecontext = self.get_user_context(title=f'{showing_group_title} | MyVkFeed')
        return dict(list(context.items()) + list(basecontext.items()))


def settings(request):
    return render(request, 'main/settings.html', {'title': 'Настройки', 'version': VERSION})


def start_page(request):
    return render(request, 'main/start_page.html', {'title': 'MyVkFeed'})


def about(request):
    return render(request, 'main/about.html', {'title': 'О сайте', 'version': VERSION})


def project_history(request):
    return render(request, 'main/project_history.html', {'title': 'История проекта', 'version': VERSION})


def page_not_found(request, exception):
    logger.error(f'Ошибка 404: {request}')
    return render(request, 'main/404.html')

handler404 = page_not_found