from django.urls import path
from .views import TaskListView, NextTaskView, CollectorStatusView, CollectView, PayView

urlpatterns = [
    path('<int:userId>/tasks', TaskListView.as_view(), name='task_list'),
    path('<int:userId>/next_task', NextTaskView.as_view(), name='next_task'),
    path('<int:userId>/status', CollectorStatusView.as_view(), name='collector_status'),
    path('<int:userId>/collect', CollectView.as_view(), name='collect'),
    path('<int:userId>/pay', PayView.as_view(), name='pay'),
]
