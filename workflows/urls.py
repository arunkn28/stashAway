from django.urls import path

from . import views

urlpatterns = [
    path('workflows/', views.WorkFlowsAPI.as_view(), name='workflows'),
    path('workflows/<slug:workflowId>/', views.UpdateWorkFlowAPI.as_view(), name='workflow-status-update')
]