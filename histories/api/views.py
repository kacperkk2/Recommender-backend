from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HistoryElementSerializer
from src.recommender_utils import user_history


class HistoriesView(APIView):

    def get(self, request, *args, **kw):
        data_set = request.GET.get('data_set', None)
        user_id = int(request.GET.get('user_id', None))

        payload = user_history(data_set, user_id)

        serializer = HistoryElementSerializer(payload, many=True)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response
