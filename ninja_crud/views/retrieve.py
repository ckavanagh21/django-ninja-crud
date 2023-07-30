from http import HTTPStatus
from typing import Any, Callable, List, Type

from django.db.models import Model, QuerySet
from django.http import HttpRequest
from ninja import Router, Schema

from ninja_crud.views import utils
from ninja_crud.views.abstract import AbstractModelView


class RetrieveModelView(AbstractModelView):
    """
    A view for retrieving a single instance of a Django model.

    This class creates a Ninja route for retrieving an object by its primary key
    and serializing it using the specified output schema.

    Attributes:
        output_schema: The Ninja Schema class used to serialize the retrieved object.
        queryset_getter: A callable to get the QuerySet for retrieving the object, or None to use the model's default manager.
        decorators: A list of decorators to apply to the view function.

    Methods:
        register_route: Register the retrieve route with the given router and model class.
        get_queryset: Get the QuerySet for retrieving the object.
        get_path: Get the URL path for the retrieve route.
    """

    def __init__(
        self,
        output_schema: Type[Schema],
        queryset_getter: Callable[[Any], QuerySet[Model]] = None,
        decorators: List[Callable] = None,
    ) -> None:
        """
        Initialize a RetrieveModelView.

        Args:
            output_schema: The Ninja Schema class used to serialize the retrieved object.
            queryset_getter: An optional callable that takes an object ID and returns a QuerySet for retrieving the object.
            decorators: A list of decorators to apply to the view function.
        """
        super().__init__(decorators=decorators)
        self.output_schema = output_schema
        self.queryset_getter = queryset_getter

    def register_route(self, router: Router, model_class: Type[Model]) -> None:
        """
        Register the retrieve route with the given router and model class.

        Args:
            router: The Ninja Router instance to which the route should be added.
            model_class: The Django model class for which the route should be created.
        """

        @router.get(
            path=self.get_path(),
            response=self.output_schema,
            operation_id=f"retrieve_{utils.to_snake_case(model_class.__name__)}",
            summary=f"Retrieve {model_class.__name__}",
        )
        @utils.merge_decorators(self.decorators)
        def retrieve_model(request: HttpRequest, id: utils.get_id_type(model_class)):
            queryset = self.get_queryset(model_class, id)
            instance = queryset.get(pk=id)
            return HTTPStatus.OK, instance

    def get_queryset(self, model_class: Type[Model], id: Any = None) -> QuerySet[Model]:
        """
        Get the QuerySet for retrieving the object.

        Args:
            model_class: The Django model class for which the QuerySet should be obtained.
            id: An optional object ID to use with the queryset_getter.

        Returns:
            A QuerySet for retrieving the object.
        """
        if self.queryset_getter is None:
            return model_class.objects.get_queryset()
        else:
            return self.queryset_getter(id)

    def get_path(self) -> str:
        """
        Get the URL path for the retrieve route.

        Returns:
            A string representing the URL path.
        """
        return "/{id}"
