from django.forms import ModelForm, ModelChoiceField, Textarea

from main.models import Course
from main_posts.models import Post


class CourseModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.short_name


class CreatePostForm(ModelForm):
    course = CourseModelChoiceField(queryset=Course.objects.all().order_by('name'))

    class Meta:
        model = Post
        widgets = {
            'content': Textarea(attrs={'cols': 80, 'rows': 15}),
            'title': Textarea(attrs={'cols': 80, 'rows': 2})
        }
        fields = ['title', 'content', 'general_post', 'course']
