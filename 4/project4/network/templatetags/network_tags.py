from django import template

from network.models import Post


register = template.Library() 


@register.filter(name="liked")
def liked(post_id, user_id):
    return Post.objects.get(id__exact=post_id) \
        .likes.filter(user__id=user_id).exists()


@register.filter(name="concat")
def concat(first, second):
    return first + str(second)
