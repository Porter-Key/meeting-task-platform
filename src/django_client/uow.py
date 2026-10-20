from __future__ import annotations

from contextlib import nullcontext
from functools import wraps
from typing import Any, Callable, TypeVar

from django.db import connection
from django.db import transaction

T = TypeVar("T")


class UnitOfWork:
    def atomic(self):
        return transaction.atomic()

    def maybe_atomic(self):
        return nullcontext() if connection.in_atomic_block else transaction.atomic()

    def wrap(self, func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> T:
            with self.atomic():
                return func(*args, **kwargs)

        return inner


uow = UnitOfWork()


def atomic():
    return uow.atomic()


def maybe_atomic():
    return uow.maybe_atomic()
