from django.urls import path

from .views import (update_model_detail_view, UpdateDetailView, JsonView, SerializerListView,
                    SerializerDetailsView)


urlpatterns = [
    path('', update_model_detail_view, name='update'),
    path('class', UpdateDetailView.as_view(), name='class'),
    path('json', JsonView.as_view(), name='json'),
    path('ser', SerializerListView.as_view()),
    path('ser_det', SerializerDetailsView.as_view())
]
