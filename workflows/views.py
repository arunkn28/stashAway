import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import ApprovalSerializer, UpdateApprovalSerializer
from .models import Approval
from core.sender import RabbitMQPusher


class WorkFlowsAPI(APIView):
    """
    Class to get the pending workflows as well to create new worklows
    """
    serializer_class = ApprovalSerializer

    def get(self, request):
        data = Approval.objects.filter(status='pending')
        serialized_data = ApprovalSerializer(data, many=True)
        return Response(serialized_data.data)

    def post(self, request):
        wfs = ApprovalSerializer(data=request.data)
        wfs.is_valid(raise_exception=True)
        approvalId = wfs.create(wfs.validated_data)
        response_data = {'workflowId': approvalId, 'status': 'pending', 'created_datetime': datetime.datetime.now()}
        return Response(response_data)


class UpdateWorkFlowAPI(APIView):
    """
    Class to update the status of any workflow
    """
    serializer_class = UpdateApprovalSerializer

    def get(self, request, approvalId):
        data = Approval.objects.filter(approval_id=approvalId)
        serialized_data = UpdateApprovalSerializer(data, many=True)
        return Response(serialized_data.data)

    def put(self, request, approvalId):
        data = Approval.objects.filter(approval_id=approvalId)
        if not data:
            return Response(status=404)
        wfs = UpdateApprovalSerializer(data=request.data)
        wfs.is_valid(raise_exception=True)
        wfs.update(data[0], wfs.validated_data)
        RabbitMQPusher().push_to_queue(data) #push to queue would be the ideal scenario (Suppressed connection issue)
        return Response(wfs.validated_data)
