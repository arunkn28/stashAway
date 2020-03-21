import datetime
from rest_framework import serializers
from .models import Approval


class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approval
        exclude = ['modified_datetime', 'approved_by', 'created_datetime', 'status']

    def create(self, validated_data):
        workflowobj = Approval(**validated_data)
        workflowobj.save()
        return workflowobj.approval_id


class UpdateApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approval
        fields = ['status', 'approved_by', 'modified_datetime']
        read_only_fields = ['modified_datetime']

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status')
        instance.approved_by = validated_data.get('approved_by')
        instance.modified_datetime = datetime.datetime.now()
        instance.save()

    def validate_approved_by(self, value):
        if not value:
            raise serializers.ValidationError("Approved by is necessary")
        return value