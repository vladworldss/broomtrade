from django.views.generic.base import ContextMixin


class SearchMixin(ContextMixin):
    search = ""
    tag = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.search
        context["tag"] = self.tag
        return context
