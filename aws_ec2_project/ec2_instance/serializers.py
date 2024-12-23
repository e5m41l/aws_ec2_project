from rest_framework import serializers

class EC2InstanceSerializer(serializers.Serializer):
    cpu = serializers.IntegerField(required=True)  # Number of vCPUs
    ram = serializers.IntegerField(required=True)  # RAM in GB

