"""Custom mixins for (API) view in the whole project"""

from rest_framework import mixins, generics


class ListAPIView(generics.ListAPIView):
    """Provides a read-only list API for the model."""


class OtaskMixinDetailView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """Provides CRUD functionality for the associated model."""

    lookup_field = "pk"
    lookup_url_kwarg = "pk"

    def get(self, request, *args, **kwargs):
        """Custom get method to pass kwargs."""
        if self.kwargs.get(self.lookup_url_kwarg):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Custom post method to pass kwargs."""
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Custom put method to pass kwargs."""
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Custom patch method to pass kwargs."""
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Custom delete method to pass kwargs."""
        return self.destroy(request, *args, **kwargs)
