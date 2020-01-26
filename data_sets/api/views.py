from rest_framework.generics import ListAPIView

from ..models import DataSet
from .serializers import DataSetSerializer
from src.recommender_utils import get_data_set_info
from src.recommender_utils import get_data_sets_names
from ..models import USERS_IDS_LIST_LENGTH


class DataSetListView(ListAPIView):
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer

    def get_queryset(self):
        data_sets = get_data_sets_names()
        queryset = self.queryset.filter(name__in=data_sets)

        if len(queryset) < len(data_sets):
            for data_set in data_sets:
                if data_set not in [data.name for data in queryset]:
                    data_set_info = get_data_set_info(data_set, USERS_IDS_LIST_LENGTH)

                    DataSet.objects.create(
                        name=data_set,
                        short=data_set,
                        users_id_sample=data_set_info['users_id_sample'],
                        users_num=data_set_info['users_num'],
                        items_num=data_set_info['items_num'],
                        density=data_set_info['density'],
                        description=""
                    )
            self.queryset = DataSet.objects.filter(name__in=data_sets)

        return self.queryset.filter(name__in=data_sets)
