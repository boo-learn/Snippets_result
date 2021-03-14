from django.forms import ModelForm
from MainApp.models import Snippet, Comment
from django.contrib.auth.models import User


class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        # Описываем поля, которые будем заполнять в форме
        fields = ['name', 'lang', 'code', 'public']


class UserForm(ModelForm):
    class Meta:
        model = User
        # Описываем поля, которые будем заполнять в форме
        fields = ['username', 'email', 'password']

    def save(self, *args, **kwargs):
        kwargs["commit"] = False
        user = super(UserForm, self).save(*args, **kwargs)
        user.is_active = True
        user.set_password(user.password)
        user.save()


class CommentForm(ModelForm):
   class Meta:
       model = Comment
       fields = ['text']