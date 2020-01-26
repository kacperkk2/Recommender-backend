from rest_framework.generics import ListAPIView

from ..models import Algorithm
from .serializers import AlgorithmSerializer
from src.recommender_utils import get_algorithms_names


class AlgorithmListView(ListAPIView):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmSerializer

    def get_queryset(self):
        algorithms = get_algorithms_names()
        queryset = self.queryset.filter(short__in=algorithms)

        if len(queryset) < len(algorithms):
            for algorithm in algorithms:
                if algorithm not in [alg.short for alg in queryset]:
                    Algorithm.objects.create(
                        name=algorithm,
                        short=algorithm,
                        description="",
                        link=""
                    )
            self.queryset = Algorithm.objects.filter(short__in=algorithms)

        return self.queryset.filter(short__in=algorithms)


