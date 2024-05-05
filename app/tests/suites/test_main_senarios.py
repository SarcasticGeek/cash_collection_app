from datetime import datetime
from django.test import TestCase
from cash_collection.models import Task, Transaction, User, Customer
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
        self.assertIn(transaction, self.collector.collected_transactions.all())
