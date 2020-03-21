from django.urls import path

from . import views

urlpatterns = [
    path('approvals/', views.WorkFlowsAPI.as_view(), name='approvals'),
    path('approvals/<slug:approvalId>/', views.UpdateWorkFlowAPI.as_view(), name='approval-status-update')
]