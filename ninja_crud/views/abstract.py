from abc import ABC, abstractmethod
from typing import Callable, List, Type

from django.db.models import Model
from ninja import Router


class AbstractModelView(ABC):
    """
    Abstract base class for creating model views.

    This class provides the interface and common functionality for specific
    model views and must be subclassed by concrete implementations.

    Attributes:
        decorators: A list of callable decorators to be applied to the model view.

    Methods:
        register_route: Abstract method to register a model route.
        get_path: Abstract method to retrieve the path associated with the view.
    """

    def __init__(self, decorators: List[Callable] = None) -> None:
        """
        Initialize the abstract model view with an optional list of decorators.

        Args:
            decorators: A list of callables that are used as decorators for the view.
                        Defaults to an empty list if not provided.
        """
        if decorators is None:
            decorators = []
        self.decorators = decorators

    @abstractmethod
    def register_route(
        self, router: Router, model_class: Type[Model]
    ) -> None:  # pragma: no cover
        """
        Abstract method to register the view's route with the given router.

        Args:
            router: The Ninja Router instance to which the route should be added.
            model_class: The Django model class associated with the view.

        Raises:
            NotImplementedError: This method must be implemented by a subclass.
        """
        pass

    @abstractmethod
    def get_path(self) -> str:  # pragma: no cover
        """
        Abstract method to retrieve the path associated with the view.

        Returns:
            A string representing the path.

        Raises:
            NotImplementedError: This method must be implemented by a subclass.
        """
        pass
