import datetime
from rest_framework import serializers
from .models import Workflow


class WorkFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        exclude = ['modified_datetime', 'approved_by', 'created_datetime', 'status']

    def create(self, validated_data):
        workflowobj = Workflow(**validated_data)
        workflowobj.save()
        return workflowobj.approval_id


class UpdateWorkFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
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