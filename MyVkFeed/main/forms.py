from django import forms

from .models import *


class FiltersForm(forms.Form):
    group_choices = [
        [group_obj.group_title, group_obj.is_hidden]
        for group_obj in Group.objects.all()
    ]
    group_title = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={"required": False}),
        choices=group_choices,
    )


class PostSearchForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text"]
        widgets = {
            "text": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "size": 70,
                    "placeholder": "Поиск постов по тексту...",
                    "name": "post-search",
                    "required": False,
                }
            )
        }


class SubsSearchForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["group_title"]
        widgets = {
            "group_title": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "size": 70,
                    "placeholder": "Введите название группы...",
                    "name": "subs-search",
                    "required": False,
                }
            )
        }
