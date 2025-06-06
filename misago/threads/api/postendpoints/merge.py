from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext
from rest_framework.response import Response

from ....acl.objectacl import add_acl_to_obj
from ...serializers import MergePostsSerializer, PostSerializer


def posts_merge_endpoint(request, thread):
    if not thread.acl["can_merge_posts"]:
        raise PermissionDenied(
            pgettext("posts api", "You can't merge posts in this thread.")
        )

    serializer = MergePostsSerializer(
        data=request.data,
        context={
            "settings": request.settings,
            "thread": thread,
            "user_acl": request.user_acl,
        },
    )

    if not serializer.is_valid():
        # Fix for KeyError - errors[0]
        errors = list(serializer.errors.values())[0]
        try:
            return Response({"detail": errors[0]}, status=400)
        except KeyError:
            return Response({"detail": list(errors.values())[0][0]}, status=400)

    posts = serializer.validated_data["posts"]
    first_post, merged_posts = posts[0], posts[1:]

    for post in merged_posts:
        post.merge(first_post)
        post.delete()

    first_post.set_search_document(thread, "fixme")
    first_post.save()

    first_post.set_search_vector()
    first_post.save(update_fields=["search_vector"])

    thread.synchronize()
    thread.save()

    thread.category.synchronize()
    thread.category.save()

    first_post.thread = thread
    first_post.category = thread.category

    add_acl_to_obj(request.user_acl, first_post)

    return Response(PostSerializer(first_post, context={"user": request.user}).data)
