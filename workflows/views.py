import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import WorkFlowSerializer, UpdateWorkFlowSerializer
from .models import Workflow
from core.sender import RabbitMQPusher


class WorkFlowsAPI(APIView):
    """
    Class to get the pending workflows as well to create new worklows
    """
    serializer_class = WorkFlowSerializer

    def get(self, request):
        data = Workflow.objects.filter(status='pending')
        serialized_data = WorkFlowSerializer(data, many=True)
        return Response(serialized_data.data)

    def post(self, request):
        wfs = WorkFlowSerializer(data=request.data)
        wfs.is_valid(raise_exception=True)
        approvalId = wfs.create(wfs.validated_data)
        response_data = {'workflowId': approvalId, 'status': 'pending', 'created_datetime': datetime.datetime.now()}
        return Response(response_data)


class UpdateWorkFlowAPI(APIView):
    """
    Class to update the status of any workflow
    """
    serializer_class = UpdateWorkFlowSerializer

    def get(self, request, approvalId):
        data = Workflow.objects.filter(approval_id=approvalId)
        serialized_data = UpdateWorkFlowSerializer(data, many=True)
        return Response(serialized_data.data)

    def put(self, request, approvalId):
        data = Workflow.objects.filter(approval_id=approvalId)
        if not data:
            return Response(status=404)
        wfs = UpdateWorkFlowSerializer(data=request.data)
        wfs.is_valid(raise_exception=True)
        wfs.update(data[0], wfs.validated_data)
        RabbitMQPusher().push_to_queue(data) #push to queue would be the ideal scenario (Suppressed connection issue)
        return Response(wfs.validated_data)
