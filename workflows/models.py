from datetime import datetime
from django.db import models


class Workflow(models.Model):
    STATUS = (
        ('pending', 'PENDING'),
        ('approved', 'APPROVED'),
        ('rejected', 'REJECTED')
    )
    workflow_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=60)
    description = models.CharField(max_length=60)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default='pending'
    )
    created_datetime = models.DateTimeField(default=datetime.now, blank=True)
    approved_by = models.CharField(max_length=30, blank=True)
    modified_datetime = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.workflow_id)