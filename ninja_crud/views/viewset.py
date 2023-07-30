from __future__ import annotations

from typing import Type

from django.db.models import Model
from ninja import Router

from ninja_crud.views import AbstractModelView


class ModelViewSetMeta(type):
    """
    Metaclass for validating ModelViewSet classes.

    This metaclass ensures that any subclass of ModelViewSet has a proper model_class attribute.

    Methods:
        validate_model_class: Validate the model_class attribute of the class.
    """

    @staticmethod
    def validate_model_class(
        new_cls: ModelViewSetMeta,
    ):  # pragma: no cover
        """
        Validate that the given class has a model_class attribute that is a subclass of django.db.models.Model.

        Args:
            new_cls: The class being validated.

        Raises:
            ValueError: If the model_class attribute is missing or not a subclass of Model.
        """
        cls_attr_name = "model_class"
        if not hasattr(new_cls, cls_attr_name):
            raise ValueError(
                f"{new_cls.__name__}.{cls_attr_name} class attribute must be set"
            )
        cls_attr_value = getattr(new_cls, cls_attr_name)
        if not isinstance(cls_attr_value, type) or not issubclass(
            cls_attr_value, Model
        ):
            raise ValueError(
                f"{new_cls.__name__}.{cls_attr_name} must be a subclass of django.db.models.Model"
            )

    def __new__(mcs, name, bases, attrs):
        """
        Create a new class instance and validate its model_class attribute.

        Args:
            name: The name of the class being created.
            bases: The base classes for the new class.
            attrs: The attributes of the new class.

        Returns:
            The created class.
        """
        new_cls = super().__new__(mcs, name, bases, attrs)

        if name != "ModelViewSet":
            mcs.validate_model_class(new_cls)

        return new_cls


class ModelViewSet(metaclass=ModelViewSetMeta):
    """
    Base class for creating view sets for Django models.

    Subclasses must set the model_class attribute to the Django model class
    they are working with.

    Class Attributes:
        model_class: The Django model class for this view set.

    Methods:
        register_routes: Register the view set's routes with the given router.
    """

    model_class: Type[Model]

    @classmethod
    def register_routes(cls, router: Router) -> None:
        """
        Register the view set's routes with the given router.

        This method iterates over all attributes of the class, looking for instances of
        AbstractModelView, and registers their routes with the given router using the model class.

        Args:
            router: The Ninja Router instance to which the routes should be added.
        """
        for attr_name in dir(cls):
            attr_value = getattr(cls, attr_name)
            if isinstance(attr_value, AbstractModelView):
                attr_value.register_route(router, cls.model_class)
