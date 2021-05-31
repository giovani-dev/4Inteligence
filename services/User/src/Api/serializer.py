from rest_framework import (
    serializers, 
    status
)
from rest_framework.exceptions import (
    ValidationError, 
    AuthenticationFailed
)
from Api.models import (
    Profile,
    Login
)
from validate_docbr import CPF
from util.validations import Validate


class Loginserializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)

    class Meta:
        model = Login
        fields = [
            'identifier',
            'email',
            'password'
        ]
        read_only_fieds = [
            'identifier'
        ]


class ProfileDetailSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.context.get('cep', None).map_fields(
                fields={
                    'logradouro': 'address', 
                    'bairro': 'district',
                    'localidade': 'city',
                    'uf': 'state'
                }
            )
        except AttributeError:
            pass

    class Meta:
        model = Profile
        fields = [
            'identifier',
            'registration_date',
            'full_name',
            'birth_date',
            'cpf',
            'cep',
            'address',
            'house_number',
            'district',
            'city',
            'state'
        ]
        extra_kwargs = {
            'identifier': {'required': True},
            'full_name': {'required': True},
            'birth_date': {'required': True},
            'cpf': {'required': True},
            'cep': {'required': True},
            'house_number': {'required': True},
        }

    def validate_cpf(self, data: str) -> str:
        Validate.conditional(
            exp=(not CPF().validate(data)),
            action=ValidationError("Invalid Value."),
            _raise=True
        )
        return data

    def validate_cep(self, data: str) -> str:
        Validate.conditional(
            exp=(not self.context['cep'].is_valid),
            action=ValidationError("Invalid Value -."), 
            _raise=True
        )
        return data

    def validate_address(self, data):
        if not data == '':
            self.context['cep'].data['address'] = data
        return data

    def validate_city(self, data: str) -> str:
        Validate.conditional(
            exp=(not data == "" and data != self.context['cep'].data['city']),
            action=ValidationError("Invalid city."), 
            _raise=True
        )
        return data

    def validate_state(self, data: str) -> str:
        Validate.conditional(
            exp=(not data == "" and data != self.context['cep'].data['state']),
            action=ValidationError("Invalid state"), 
            _raise=True
        )
        return data

    def validate_district(self, data: str) -> str:
        Validate.conditional(
            exp=(not data == "" and data != self.context['cep'].data['district']),
            action=ValidationError("Invalid district"), 
            _raise=True
        )
        return data

    def update(self, instance, validated_data):
        validated_data.update(self.context['cep'].data)
        return super(ProfileDetailSerializer, self).update(instance, validated_data)


class ProfileSerializer(ProfileDetailSerializer):
    login = Loginserializer(many=False, write_only=True, required=True)
    full_name = serializers.CharField(required=True)

    class Meta:
        model = Profile
        fields = [
            'identifier',
            'full_name',
            'birth_date',
            'cpf',
            'cep',
            'address',
            'district',
            'city',
            'state',
            'house_number',
            'login',
        ]
        read_only_fields = [
            'identifier'
        ]
        extra_kwargs = {
            'identifier': {'required': True},
            'full_name': {'required': True},
            'birth_date': {'required': True},
            'cpf': {'required': True},
            'cep': {'required': True},
            'house_number': {'required': True},
        }


    def create(self, validated_data: dict) -> object:
        validated_data.update(self.context['cep'].data)
        login_data = validated_data.pop('login')
        login_instance = Login.objects.create_user(**login_data)
        try:
            profile_instance = self.Meta.model.objects.create(login=login_instance, **validated_data)
        except Exception as e:
            login_instance.delete()
            raise e
        return profile_instance