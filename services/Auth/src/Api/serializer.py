from rest_framework import (
    serializers, 
    status
)
from rest_framework.exceptions import (
    ValidationError, 
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied
)
from rest_framework_jwt.utils import jwt_decode_handler
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidSignatureError
)
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import FieldDoesNotExist
from Models.User.models import Login


class AuthfieldSerializer(serializers.Serializer):
    field = serializers.CharField(required=True, max_length=25, min_length=5)
    value = serializers.BooleanField(required=True)

    def validate(self, attrs: dict):
        try:
            Login._meta.get_field(attrs['field'])
        except FieldDoesNotExist:
            raise ValidationError({
                attrs['field']: 'Invalid Field.'
            })
        return attrs


class AvaibleMethodSerializar(serializers.Serializer):
    request_method: object = serializers.CharField(required=True, write_only=True, max_length=25)
    avaible_methods: object = serializers.ListField(
        child=serializers.CharField(max_length=25),
        required=True, 
        write_only=True
    )
        
    def validate_request_method(self, attr, in_validate: bool = False):
        errors = list()
        request_methods = ['GET','OPTIONS','HEAD','POST','PUT','PATCH','DELETE']
        if not attr.upper() in request_methods:
            errors.append(f"This method {attr} is not exist.")
        if len(errors) >= 1 and not in_validate:
            raise ValidationError(errors)
        elif len(errors) >= 1 and in_validate:
            return errors
        elif in_validate:
            return errors
        else:
            return attr

    def validate_avaible_methods(self, attr):
        errors: list = list()
        for method in attr:
            get_error = self.validate_request_method(attr=method, in_validate=True)
            try:
                errors.append(get_error[0])
            except IndexError:
                pass
        if len(errors) >= 1:
            raise ValidationError(errors)
        return attr

    def validate(self, attrs: dict) -> object:
        errors = list()
        
        # request_method: list = self.validate_request_method(attr=attrs['request_method'], in_validate=True)
        unavailable_request_method = list()
        if not attrs['request_method'] in attrs['avaible_methods']:
            unavailable_request_method.append(f"Unavailable method {attrs['request_method']}.")
        if len(unavailable_request_method) >= 1:
            raise ValidationError({'request_method': unavailable_request_method})
        return attrs


class AuthUserSerializer(serializers.Serializer):
    token: object = serializers.CharField(required=True, write_only=True)
    to_validate: object = AuthfieldSerializer(many=True, required=True, write_only=True)
    method: object = AvaibleMethodSerializar(required=False, write_only=True)

    class Meta:
        fields = [
            'token',
            'to_validate',
            'is_authed',
            'method'
        ]

    def validate(self, attrs: dict) -> bool:
        try:
            handler = jwt_decode_handler(attrs['token'])
        except (ExpiredSignatureError, InvalidSignatureError):
            raise AuthenticationFailed()
        user = Login.objects.get(email=handler['email'])
        for validate in attrs['to_validate']:
            if not user.is_valid_field(field=validate['field'], value=validate['value']):
                raise PermissionDenied()
        return attrs