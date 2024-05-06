from .models import Task, Transaction, FrozenCollector, ManagerLog
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum

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
    def create_transaction(collector = None, manager = None, amount = 0):
        transaction = Transaction.objects.create(manager=manager, collector=collector, amount=amount, timestamp=timezone.now(), payment_date = timezone.now())

        return transaction
    
    @staticmethod
    def pay_unpaid_transaction(collector = None, manager = None, amount = 0):
        unpaid_transactions = Transaction.objects.filter(manager=manager, collector=collector, is_paid=False)
        if unpaid_transactions.exists():
            # Calculate the total amount of unpaid transactions
            total_amount = unpaid_transactions.aggregate(total=Sum('amount'))['total']
            remaining_amount = amount
            if total_amount <= amount:
                # Pay all unpaid transactions
                for transaction in unpaid_transactions:
                    if remaining_amount < transaction.amount:
                        break
                    transaction.is_paid = True
                    transaction.payment_date = timezone.now()
                    transaction.save()
                    remaining_amount -= transaction.amount


class UserService:
    @staticmethod
    def mark_collector_frozen(collector, start_date = None):
        if start_date is None:
            start_date = timezone.now()

        # Calculate the end date (2 days from the start date)
        end_date = start_date + timedelta(days=2)

        # Check if the collector has unpaid transactions exceeding 5000USD between start_date and end_date
        total_amount = collector.collected_transactions.filter(timestamp__range=(start_date, end_date), is_paid=False).aggregate(total=Sum('amount'))['total']

        if total_amount and total_amount >= 5000 and end_date >= start_date + timedelta(days=2):
            # Mark the collector as frozen
            FrozenCollector.objects.get_or_create(collector=collector, frozen_since=timezone.now())
            return True
        else:
            return False

    @staticmethod
    def is_collector_frozen(collector):
        return FrozenCollector.objects.filter(collector=collector).exists()
    
    @staticmethod
    def remove_collector_from_frozen(collector):
        frozen_collector = FrozenCollector.objects.get(collector=collector)
        frozen_collector.delete()  # Remove the FrozenCollector entry


class ManagerLogService:
    @staticmethod
    def log_manager_action(manager, action):
        ManagerLog.objects.create(manager=manager, action=action)
