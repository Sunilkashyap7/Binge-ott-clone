from user_app.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def save(self):

        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError(
                {'status': 'failed', 'message': 'Your password and confirmation password do not match. ', })

        account = User(
            email=self.validated_data['email'], name=self.validated_data['name'], mobile_number=self.validated_data['mobile_number'])
        account.set_password(password)
        account.save()

        return account
