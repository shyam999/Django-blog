from rest_framework import serializers
from core.models import Post


class PostSerializer(serializers.ModelSerializer):
    
    """Serializer to map the Post Model instance into JSON format."""

    class Meta:
        """Map the serializer to a model and their fields."""
        model = Post
        fields = ['id', 'title', 'author', 'created_date']
