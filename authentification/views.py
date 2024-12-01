from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth.models import User


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
        })


# Example of a protected API endpoint
class ProtectedView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        content = {
            'user': str(request.user),
            'auth': str(request.auth),
        }
        return Response(content)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if old_password and new_password:
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Please provide both old and new passwords.'}, status=status.HTTP_400_BAD_REQUEST)
