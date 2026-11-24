from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Opportunity, Report, Appeal
from .serializers import (
    RegistrationSerializer, PublicUserSerializer, PostSerializer,
    OpportunitySerializer, ReportSerializer, AppealSerializer,
)
from .permissions import IsOwnerOrReadOnly

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data["username"])
        token, _ = Token.objects.get_or_create(user=user)
        response.data["token"] = token.key
        return response

class LoginTokenView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        from django.contrib.auth import authenticate
        user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
        if not user:
            return Response({"detail": "Invalid credentials."}, status=400)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})

class ProfileListView(generics.ListAPIView):
    queryset = User.objects.filter(is_active=True).order_by("username")
    serializer_class = PublicUserSerializer
    permission_classes = [AllowAny]

class ProfileDetailView(generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = PublicUserSerializer
    permission_classes = [AllowAny]

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    def get_queryset(self):
        return Post.objects.filter(is_hidden=False).select_related("author")
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class OpportunityViewSet(viewsets.ModelViewSet):
    serializer_class = OpportunitySerializer
    permission_classes = [IsOwnerOrReadOnly]
    def get_queryset(self):
        return Opportunity.objects.filter(is_open=True).select_related("publisher")
    def perform_create(self, serializer):
        serializer.save(publisher=self.request.user)

class ReportCreateView(generics.CreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

class AppealCreateView(generics.CreateAPIView):
    serializer_class = AppealSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Appeal.objects.filter(user=self.request.user)
