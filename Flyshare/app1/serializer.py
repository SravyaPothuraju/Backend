from app1.models import PostModel
from rest_framework.serializers import ModelSerializer

class PostModelSerializer(ModelSerializer):
    class Meta:
        model = PostModel
        fields = '__all__'