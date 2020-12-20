from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

class AdminSerializer(serializers.ModelSerializer):
    """Model Serializer for admin objects"""

    class Meta:
        model = get_user_model()
        fields = ('username', 'name', 'address', 'phone', 'postal_code', 'birth_date', 
                  'email', 'is_staff', 'password',
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 6
            }
        }
    
    def create(self, validated_data):
        """To use the create_user function and creat an admin with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """The Serializer class for the admin authentication object"""
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type':'password'}, 
        trim_whitespace=False
    )

    def validate(self, attrs):
        """To validate and authenticate the admin request attributes"""
        username = attrs.get('username')
        password = attrs.get('password')
        admin = authenticate(
            request=self.context.get('requset'),
            username=username,
            password=password
        )
        if not admin:
            msg = "Unable to authenticate Admin with provided credentials."
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = admin
        return attrs