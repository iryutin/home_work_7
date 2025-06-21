from rest_framework import serializers
from user.models import Payments

class PaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields = '__all__'