from django.test import TestCase
from .views import change_machine

# Create your tests here.
class ChangeTests(TestCase):

    def test_exact_change_given(self):
        """exact_change returns True if exact change is given"""

        item_cost = 10.52
        amount_paid = 10.52


