from datetime import datetime, timedelta
from django.test import TestCase
from cash_collection.models import Task, Transaction, User
from cash_collection.services import TaskService, TransactionService, UserService

class CashCollectorTestCase(TestCase):
    def tearDown(self):
        Transaction.objects.all().delete()
        Task.objects.all().delete()
        User.objects.all().delete()

    def setUp(self):
        # Create a test CashCollector
        self.collector = User.objects.create(username='John')
        self.manager = User.objects.create(username='test_manager')


    def test_collection_transactions(self):
        start_date = datetime(2000, 1, 1, 6, 0)
        # Simulate collection transactions by John
        # Collected 1000USD at 2000-01-01 06:00
        Transaction.objects.create(collector=self.collector, manager=self.manager, amount=1000, timestamp=datetime(2000, 1, 1, 6, 0))
        self.collector.refresh_from_db()

        # Collected 6000USD at 2000-01-01 07:00
        Transaction.objects.create(collector=self.collector, manager=self.manager, amount=6000, timestamp=datetime(2000, 1, 1, 7, 0))
        self.collector.refresh_from_db()
        # Collected 2000USD at 2000-01-02 08:00
        Transaction.objects.create(collector=self.collector, manager=self.manager, amount=2000, timestamp=datetime(2000, 1, 2, 8, 0))

        # Check if John is not frozen initially
        self.collector.refresh_from_db()
        UserService.mark_collector_frozen(self.collector, start_date)
        self.collector.refresh_from_db()
        self.assertFalse(UserService.is_collector_frozen(self.collector))

        # Collected at 2000-01-03 06:00, John is still not frozen
        self.collector.refresh_from_db()
        Transaction.objects.create(collector=self.collector, manager=self.manager, amount=2000, timestamp=datetime(2000, 1, 3, 6, 0))
        UserService.mark_collector_frozen(self.collector,  start_date)
        self.assertFalse(UserService.is_collector_frozen(self.collector))

        # Collected at 2000-01-03 07:00, John is now frozen
        self.collector.refresh_from_db()
        Transaction.objects.create(collector=self.collector, manager=self.manager, amount=2000, timestamp=datetime(2000, 1, 3, 7, 0))
        UserService.mark_collector_frozen(self.collector, start_date)

        self.assertTrue(UserService.is_collector_frozen(self.collector))

    def test_next_task_for_collector(self):
        # Create tasks for John
        Task.objects.create(collector=self.collector, customer_name='Customer 1', amount_due=1000, amount_due_at=datetime(2000, 1, 1, 6, 0))
        Task.objects.create(collector=self.collector, customer_name='Customer 2', amount_due=2000, amount_due_at=datetime(2000, 1, 1, 7, 0))
        Task.objects.create(collector=self.collector, customer_name='Customer 3', amount_due=500, amount_due_at=datetime(2000, 1, 2, 8, 0))

        # John should only see the first task initially
        next_task = TaskService.get_next_task_for_collector(self.collector)
        self.assertEqual(next_task.customer_name, 'Customer 1')

        # Advance time by 24 hours
        new_time = datetime(2000, 1, 2, 7, 0)
        Task.objects.filter(collector=self.collector).update(amount_due_at=new_time)

        # Now John should see the second task
        next_task = TaskService.get_next_task_for_collector(self.collector)
        self.assertEqual(next_task.customer_name, 'Customer 2')

        # Advance time by another 24 hours
        new_time = datetime(2000, 1, 3, 7, 0)
        Task.objects.filter(collector=self.collector).update(amount_due_at=new_time)

        # Now John should not see any tasks as he is frozen
        next_task = TaskService.get_next_task_for_collector(self.collector)
    #     self.assertIsNone(next_task)

class TransactionTestCase(TestCase):
    def setUp(self):
        self.collector = User.objects.create(username='John')
        self.manager = User.objects.create(username='test_manager')

    def test_create_transaction(self):
        # Create a transaction for the collector
        transaction = Transaction.objects.create(
            collector=self.collector,
            manager=self.manager,
            amount=2000,
            timestamp=datetime(2000, 1, 3, 7, 0)
        )

        # Refresh the collector object
        self.collector.refresh_from_db()

        # Check if the transaction is associated with the collector
        print(self.collector.collected_transactions.all())
        self.assertIn(transaction, self.collector.collected_transactions.all())
