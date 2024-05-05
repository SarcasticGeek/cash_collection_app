from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task, Transaction
from .serializers import TaskSerializer, TransactionSerializer
from .services import TaskService, TransactionService, UserService

class TaskListView(APIView):
    def get(self, request):
        tasks = Task.objects.filter(completed=True)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

class NextTaskView(APIView):
    def get(self, request):
        collector = request.user  # Assuming authenticated user is the CashCollector
        next_task = TaskService.get_next_task_for_collector(collector)
        serializer = TaskSerializer(next_task)
        return Response(serializer.data)

class CollectorStatusView(APIView):
    def get(self, request):
        collector = request.user  # Assuming authenticated user is the CashCollector
        frozen = UserService.is_collector_frozen(collector)
        return Response({'frozen': frozen})

class CollectView(APIView):
    def post(self, request):
        amount = request.data.get('amount')
        task_id = request.data.get('task_id')
        collector = request.user  # Assuming authenticated user is the CashCollector

        TransactionService.create_transaction(collector, amount)
        TaskService.mark_task_completed(task_id)

        return Response(status=status.HTTP_201_CREATED)

class PayView(APIView):
    def post(self, request):
        amount = request.data.get('amount')
        manager = request.user  # Assuming authenticated user is the Manager

        TransactionService.create_transaction(manager, amount)

        return Response(status=status.HTTP_201_CREATED)
