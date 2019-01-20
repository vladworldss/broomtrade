from django.views.generic.base import View


class PageNumberView(View):

    def get(self, request, *args, **kwargs):
        # этот блок нужен для сортировки и поиска товара - был добавлен ранее
        self.sort = self.request.GET.get("sort", "0")
        self.order = self.request.GET.get("order", "A")
        self.search = self.request.GET.get("search", '')

        self.tag = self.request.GET.get("tag", '')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pn = request.GET.get("page", '1')
        self.success_url = self.success_url + "?page=" + pn
        try:
            self.success_url = self.success_url + "&search=" + request.GET["search"]
        except KeyError:
            pass
        try:
            self.success_url = self.success_url + "&tag=" + request.GET["tag"]
        except KeyError:
            pass
        return super().post(request, *args, **kwargs)
