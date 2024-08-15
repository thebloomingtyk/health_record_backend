from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # path('add_doctor/', views.add_doctor, name='add_doctor'),
    # path('add_patient/', views.add_patient, name='add_patient'),
    # path('add_consultation/', views.add_consultation, name='add_consultation'),
    path("daily_summary/", views.daily_summary, name="daily_summary"),
]


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'rooms', views.RoomViewSet)
router.register(r'consultations', views.ConsultationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/room-choices/', views.RoomChoicesView.as_view()),
    path('api/daily-summary/', views.DailySummaryReportView.as_view(), name='daily-summary'),
]

