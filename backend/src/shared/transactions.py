"""Django transaction binding. Imported only at the composition root."""

from django.db import transaction


def transaction_boundary():
    return transaction.atomic()


def after_commit(callback):
    transaction.on_commit(callback)
