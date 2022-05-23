from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from webpage.models import VisitedWebPage
from webpage.serializers import VisitedWebPageSerializer
from django.views.generic import FormView, ListView
from webpage.forms import VisitURLForm
from django.template.response import TemplateResponse
from webpage.extractor import LinkExtractor
from django.http import Http404
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

class VisitedWebPageViewSet(viewsets.ModelViewSet):

    queryset = VisitedWebPage.objects.all()
    serializer_class = VisitedWebPageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        url = request.data["url"]
        extractor = LinkExtractor()
        try:
            result = extractor.extract(url)
        except Exception as e:
            raise Http404(str(e))

        visit = VisitedWebPage(user=request.user,
                               url=url,
                               nb_http_link=result["nb_http"],
                               nb_tel_link=result["nb_tel"],
                               nb_mail_link=result["nb_email"],
                               )
        visit.save()
        data = VisitedWebPageSerializer(visit).data
        data.update(result)
        return Response(data)


class VisitWebPagetFormView(FormView):

    template_name = 'webpage/generic_form.html'
    form_class = VisitURLForm

    def form_valid(self, form):
        url = form.cleaned_data["url"]
        extractor = LinkExtractor()
        try:
            result = extractor.extract(url)
        except Exception as e:
            raise Http404(str(e))

        if self.request.user.is_anonymous:
            user, _ = User.objects.get_or_create(username="test", defaults={"username": "test"})
        else:
            user = self.request.user
        user.set_password("test")
        user.save()
        visit = VisitedWebPage(user=user,
                               url=url,
                               nb_http_link=result["nb_http"],
                               nb_tel_link=result["nb_tel"],
                               nb_mail_link=result["nb_email"],
                               )
        visit.save()
        result["url_hash"] = visit.url_hash

        return TemplateResponse(self.request, 'webpage/result.html', {"data": result})


class HistoryListView(ListView):

    def get_queryset(self):
        if self.request.user.is_anonymous:
            user, _ = User.objects.get_or_create(username="test", defaults={"username": "test"})
        else:
            user = self.request.user
        user.set_password("test")
        user.save()
        return VisitedWebPage.objects.filter(user=user, url_hash=self.kwargs["urlId"]).order_by("visited_at")

