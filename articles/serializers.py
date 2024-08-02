from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    is_visible = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'visibility', 'is_visible']
        read_only_fields = ['author']

    def get_is_visible(self, obj):
        request = self.context.get('request')
        if obj.visibility == Article.PUBLIC:
            return True
        if request and request.user.is_authenticated:
            if obj.author == request.user:
                return True
            if obj.visibility == Article.PRIVATE and request.user.role == 'subscriber':
                return True
        return False

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not representation['is_visible']:
            representation['content'] = 'Содержание ограничено'
        return representation

    def create(self, validated_data):
        request = self.context['request']
        if request.user.role != 'author':
            raise serializers.ValidationError("Только авторы могут создавать статьи.")
        validated_data['author'] = request.user
        return super().create(validated_data)

