from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework import generics
from core.models import Post
from .serializers import PostSerializer

class PostListView(generics.ListAPIView):
    """
    This class defines the create view of our rest api.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

@api_view(["GET", ])
@permission_classes((permissions.AllowAny,))
def api_post_view(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)

@api_view(["POST", ])
@permission_classes((permissions.AllowAny,))
def api_create_post_view(request):
    post = Post()
    if request.method == "POST":
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT", ])
@permission_classes((permissions.AllowAny,))
def api_update_post_view(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = "update successful"
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE", ])
@permission_classes((permissions.AllowAny,))
def api_delete_post_view(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "DELETE":
        operation = post.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete was unsuccessful"
        return Response(data=data)