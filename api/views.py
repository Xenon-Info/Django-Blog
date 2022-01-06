from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import PostSerializer
from posts.models import Post, Review, Tag


@api_view(['GET'])
def get_routes(request):

    routes = [
        {'GET': '/api/posts'},
        {'GET': '/api/posts/id'},
        {'POST': '/api/posts/id/vote'},

        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]
    return Response(routes)


@api_view(['GET'])
def get_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_post(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_vote(request, pk):
    post = Post.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    review, created = Review.objects.get_or_create(
        owner=user,
        post=post,
    )

    review.value = data['value']
    review.save()
    post.getVoteCount

    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
def remove_tag(request):
    tag_id = request.data['tag']
    post_id = request.data['post']

    post = Post.objects.get(id=post_id)
    tag = Tag.objects.get(id=tag_id)

    post.tags.remove(tag)

    return Response('Tag was deleted!')
