from django.test import TestCase
from datetime import datetime, timedelta
from cash_collection.models import User, Customer
from django.contrib.auth import get_user_model  # Import the custom user model
from cash_collection.models import Task, Transaction, FrozenCollector
from cash_collection.services import TaskService, TransactionService, UserService

class TaskServiceTestCase(TestCase):
    def test_get_next_task_for_collector(self):
        # Create a test collector
        collector = User.objects.create(username='test_collector')
        customer_1 = Customer.objects.create(name='test_customer_1', amount_due=1000, amount_due_at=datetime(2000, 1, 1, 6, 0))
        customer_2 = Customer.objects.create(name='test_customer_2', amount_due=1000, amount_due_at=datetime(2000, 1, 1, 6, 0))

        # Create tasks for the collector
        task1 = Task.objects.create(collector=collector, customer=customer_1)
        task2 = Task.objects.create(collector=collector, customer=customer_2)

        # Ensure only the first task is returned as the next task
        next_task = TaskService.get_next_task_for_collector(collector)
        self.assertEqual(next_task, task1)

    def test_mark_task_completed(self):
        # Create a test task
        collector = User.objects.create(username='test_collector')
        customer_1 = Customer.objects.create(name='test_customer_1', amount_due=1000, amount_due_at=datetime(2000, 1, 1, 6, 0))
        task = Task.objects.create(collector=collector, customer=customer_1, completed=False)

        # Mark the task as completed
        TaskService.mark_task_completed(task.id)

        # Check if the task is marked as completed
        updated_task = Task.objects.get(id=task.id)
        self.assertTrue(updated_task.completed)

class TransactionServiceTestCase(TestCase):
    def test_create_transaction(self):
        # Create test users
        collector = User.objects.create(username='test_collector')
        manager = User.objects.create(username='test_manager')

        # Create a test transaction
        transaction = TransactionService.create_transaction(collector, manager, amount=100)

        # Check if the transaction is created successfully
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.collector, collector)
        self.assertEqual(transaction.manager, manager)
        self.assertEqual(transaction.amount, 100)

class UserServiceTestCase(TestCase):
    def setUp(self):
        # Get the custom user model
        User = get_user_model()

        # Create a test CashCollector
        self.collector = User.objects.create(username='John')
        self.manager = User.objects.create(username='Manager')

        
    def test_mark_collector_frozen(self):
        # Create a test collector with transactions
        # collector = User.objects.create(username='test_collector')
        # manager = User.objects.create(username='test_manager')
        for _ in range(5):
            Transaction.objects.create(collector=self.collector,manager=self.manager, amount=1000)

        # Check if the collector is marked as frozen
        UserService.mark_collector_frozen(self.collector)
        self.assertFalse(FrozenCollector.objects.filter(collector=self.collector).exists())
