from rest_framework import serializers
from .models import Pose
class PoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pose
        fields = "__all__"