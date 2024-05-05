from django.urls import path
from .views import TaskListView, NextTaskView, CollectorStatusView, CollectView, PayView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('next_task/', NextTaskView.as_view(), name='next_task'),
    path('status/', CollectorStatusView.as_view(), name='collector_status'),
    path('collect/', CollectView.as_view(), name='collect'),
    path('pay/', PayView.as_view(), name='pay'),
]
