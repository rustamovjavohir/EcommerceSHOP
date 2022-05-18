from rest_framework.serializers import ModelSerializer
from .models import User


class UserSerializers(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', "email", 'date_of_birth', 'profile_image', 'password')  # 'password'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        # if self.context['request'].user.is_staff:
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.profile_image = validated_data.get('profile_image',  instance.profile_image)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',  'password')  # 'password'
        extra_kwargs = {'password': {'write_only': True}}
