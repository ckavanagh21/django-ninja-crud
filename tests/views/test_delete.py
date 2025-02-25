from unittest.mock import MagicMock

from django.db import models
from django.test import TestCase

from ninja_crud.views import DeleteModelView
from tests.test_app.models import Collection, Item


class DeleteModelViewTest(TestCase):
    def test_register_route_router_kwargs(self):
        router_mock = MagicMock()
        model_view = DeleteModelView(router_kwargs={"exclude_unset": True})

        model_view.register_route(router_mock, Collection)

        router_mock.delete.assert_called_once()
        self.assertTrue(router_mock.delete.call_args[1]["exclude_unset"])
