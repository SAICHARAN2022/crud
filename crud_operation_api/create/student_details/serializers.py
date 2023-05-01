from rest_framework import serializers
from .models import student
class studentSerializer(serializers.ModelSerializer):
    class Meta:
        model = student
        fields = ["firstname", "lastname", "city", "phonenumber"] # alterantive '__all__'
    
    # def validate_phonenumber(self,value):
    #     if len(value) < 10:
    #         raise serializers.ValidationError("more than 10 digits entered")
    #     return value
    
    # def validate_city(self,value):
    #     if value == "assam":
    #         raise serializers.ValidationError("these region is not applicable")
    #     return value


    
    
