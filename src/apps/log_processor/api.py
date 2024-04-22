from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from .models import NginxLogEntry
from .serializers import NginxLogEntrySerializer


class NginxLogEntryViewSet(viewsets.ModelViewSet):
    queryset = NginxLogEntry.objects.all()
    serializer_class = NginxLogEntrySerializer
    pagination_class = LimitOffsetPagination
