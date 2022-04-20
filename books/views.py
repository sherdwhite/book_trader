# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views import generic


class MainView(generic.TemplateView):
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context.update({"base_api_url": self.request.build_absolute_uri("/api")})

        return context
