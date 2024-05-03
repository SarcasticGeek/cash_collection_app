from .models import Task, Transaction, FrozenCollector, ManagerLog
from datetime import timedelta
from django.utils import timezone

class TaskService:
    @staticmethod
    def get_next_task_for_collector(collector):
        return Task.objects.filter(collector=collector, completed=False).first()

    @staticmethod
    def mark_task_completed(task_id):
        task = Task.objects.get(id=task_id)
        task.completed = True
        task.save()

class TransactionService:
    @staticmethod
    def create_transaction(collector, manager, amount):
        transaction = Transaction.objects.create(collector=collector, manager=manager, amount=amount)
        return transaction



class UserService:
    @staticmethod
    def mark_collector_frozen(collector):
        if collector.collected_transactions.filter(timestamp__gte=timezone.now() - timedelta(days=2)).count() > 5000:
            FrozenCollector.objects.create(collector=collector, frozen_since=timezone.now())

    @staticmethod
    def is_collector_frozen(collector):
        return FrozenCollector.objects.filter(collector=collector).exists()


class ManagerLogService:
    @staticmethod
    def log_manager_action(manager, action):
        ManagerLog.objects.create(manager=manager, action=action)
