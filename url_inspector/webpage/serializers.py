from rest_framework import serializers
from webpage.models import VisitedWebPage


class VisitedWebPageSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = VisitedWebPage
        exclude = ['url_hash']
