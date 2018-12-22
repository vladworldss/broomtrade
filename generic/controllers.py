from django.views.generic.base import View


class PageNumberView(View):

    def get(self, request, *args, **kwargs):
      self.sort = self.request.GET.get("sort", "0")
      self.order = self.request.GET.get("order", "A")
      self.search = self.request.GET.get("search", '')
      self.tag = self.request.GET.get("tag", '')
      return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pn = request.GET.get("page", '1')
        self.success_url = self.success_url + "?page=" + pn
        self.success_url = self.success_url + "&search=" + request.GET.get("search", None)
        self.success_url = self.success_url + "&tag=" + request.GET.get("tag", None)
        return super().post(request, *args, **kwargs)
