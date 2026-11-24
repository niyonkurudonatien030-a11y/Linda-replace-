from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post, Opportunity, Report, Appeal

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=10)
    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name")
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "headline", "location", "is_verified_professional")

class PostSerializer(serializers.ModelSerializer):
    author = PublicUserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ("id", "author", "body", "created_at", "updated_at")
        read_only_fields = ("id", "author", "created_at", "updated_at")

class OpportunitySerializer(serializers.ModelSerializer):
    publisher = PublicUserSerializer(read_only=True)
    class Meta:
        model = Opportunity
        fields = ("id", "publisher", "title", "kind", "organisation", "location",
                  "description", "application_url", "deadline", "created_at", "is_open")
        read_only_fields = ("id", "publisher", "created_at")

class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Report
        fields = ("id", "reporter", "target_user", "reason", "details", "status", "created_at")
        read_only_fields = ("id", "status", "created_at")

class AppealSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Appeal
        fields = ("id", "user", "subject", "explanation", "requested_resolution", "status", "created_at")
        read_only_fields = ("id", "status", "created_at")
