from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task, Transaction, User
from .serializers import TaskSerializer, TransactionSerializer
from .services import TaskService, TransactionService, UserService

class TaskListView(APIView):
    def get(self, request, userId):
        collector = User.objects.get(id= userId)
        tasks = Task.objects.filter(completed=True, collector=collector)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

class NextTaskView(APIView):
    def get(self, request, userId):
        # collector = request.user  # Assuming authenticated user is the CashCollector
        collector = User.objects.get(id= userId)

        next_task = TaskService.get_next_task_for_collector(collector)
        serializer = TaskSerializer(next_task)
        return Response(serializer.data)

class CollectorStatusView(APIView):
    def get(self, request, userId):
        # collector = request.user  # Assuming authenticated user is the CashCollector
        collector = User.objects.get(id= userId)
        frozen = UserService.is_collector_frozen(collector)
        return Response({'frozen': frozen})

class CollectView(APIView):
    def post(self, request, userId):
        amount = request.data.get('amount')
        task_id = request.data.get('task_id')
        manager_id = request.data.get('manager_id')
        manager = User.objects.get(id= manager_id)
        # collector = request.user  # Assuming authenticated user is the CashCollector
        collector = User.objects.get(id= userId)

        if UserService.is_collector_frozen(collector):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        TransactionService.create_transaction(collector=collector,amount=amount)
        TaskService.mark_task_completed(task_id)
        UserService.mark_collector_frozen(collector)

        return Response(status=status.HTTP_201_CREATED)

class PayView(APIView):
    def post(self, request, userId):
        amount = request.data.get('amount')
        # collector = request.user  # Assuming authenticated user is the Manager
        collector = User.objects.get(id= userId)
        manager_id = request.data.get('manager_id')
        manager = User.objects.get(id= manager_id)

        TransactionService.create_transaction(manager=manager, amount=amount)
        UserService.mark_collector_frozen(collector)

        if UserService.is_collector_frozen(collector):
            UserService.remove_collector_from_frozen(collector)

        return Response(status=status.HTTP_201_CREATED)
