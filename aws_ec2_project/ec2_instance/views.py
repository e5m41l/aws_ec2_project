from .serializers import EC2InstanceSerializer
import boto3
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Mapping of CPU and RAM to EC2 instance types
INSTANCE_TYPE_MAPPING = {
    (1, 1): "t2.micro",
    (1, 2): "t2.small",
    (2, 4): "t2.medium",
    (2, 8): "m5.large",
    (4, 16): "m5.xlarge",
    (4, 32): "m5.2xlarge",
}

class EC2InstanceCreateView(APIView):
    def post(self, request, *args, **kwargs):
        # Validate and deserialize the input data
        serializer = EC2InstanceSerializer(data=request.data)
        if serializer.is_valid():
            # Extract validated data (CPU and RAM)
            cpu = serializer.validated_data['cpu']
            ram = serializer.validated_data['ram']

            # Find the nearest matching instance type
            instance_type = self.find_instance_type(cpu, ram)

            if not instance_type:
                return Response({"error": "No suitable instance type found."}, status=status.HTTP_400_BAD_REQUEST)

            # Craete EC2 client
            ec2_client = boto3.client('ec2', region_name="us-west-2")


            # I don't have any valid credentials!!!!!!!!!!!!!
            # define EC2 instance parameters
            instance_params = {
                'ImageId': 'ami-0abcdef1234567890',  # needs to be replaced with valid AMI ID
                'InstanceType': instance_type,
                'MinCount': 1,
                'MaxCount': 1,
                'KeyName': 'xyz-abc-123-name', # needs to be replaced with a key-pair name
                'SecurityGroupIds': ['sg-12345678'],
                'SubnetId': 'subnet-12345678', 
            }

            try:
                # Launch EC2 instance
                response = ec2_client.run_instances(**instance_params)
                instance_id = response['Instances'][0]['InstanceId']

                # Return a success response
                return Response({"instance_id": instance_id}, status=status.HTTP_201_CREATED)
            except Exception as e:
                # print(str(e))

                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def find_instance_type(self, cpu, ram):
        """
        find the closest instance type based on CPU and RAM.
        """
        closest_match = None

        # Iterate over the instance type mapping to find the closest one
        for (cpu_required, ram_required), instance_type in INSTANCE_TYPE_MAPPING.items():
            if cpu >= cpu_required and ram >= ram_required:
                if closest_match is None or (cpu_required, ram_required) > (cpu, ram):
                    closest_match = instance_type

        return closest_match
