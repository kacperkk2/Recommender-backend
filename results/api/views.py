from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RecommendationElementSerializer

from src.recommender_utils import recommend


class ResultsView(APIView):

    def get(self, request, *args, **kw):
        algorithm = request.GET.get('algorithm', None)
        data_set = request.GET.get('data_set', None)
        user_id = int(request.GET.get('user_id', None))
        top_k = int(request.GET.get('top_k', None))

        try:
            payload = recommend(algorithm, data_set, user_id, top_k)
            serializer = RecommendationElementSerializer(payload, many=True)
            response_data = serializer.data
        except KeyError:
            return JsonResponse({'message': "INVALID_ID"}, status=400)
        except FileNotFoundError:
            return JsonResponse({'message': "NO_MODEL"}, status=400)

        return Response(response_data, status=status.HTTP_200_OK)
