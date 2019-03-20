from rest_framework import serializers, pagination
from django.core.paginator import Paginator
from core.models import Leaderboard, Record


class RecordSerializer(serializers.ModelSerializer):
    completed_on = serializers.DateTimeField(format="%b %d %Y %X")
    rift_time = serializers.SerializerMethodField()
    class_name = serializers.SerializerMethodField()

    class Meta:
        model = Record
        fields = ('leaderboard', 'rank', 'battletag', 'class_name',
                  'rift_level', 'rift_time', 'completed_on')

    def get_rift_time(self, obj):
        """ Customizing rift duration display format """
        duration = obj.rift_time.total_seconds()
        minutes = (int)(duration / 60)
        seconds = (int)(duration % 60)
        milis = (int)(duration * 1000) % 1000
        return f'{minutes}m {seconds}.{milis}s'

    def get_class_name(self, obj):
        """ Capitalize class name """
        class_name = obj.class_name
        return class_name.title()


class LeaderboardSerializer(serializers.ModelSerializer):
    records = serializers.SerializerMethodField('paginated_records')

    class Meta:
        model = Leaderboard
        fields = ('slug', 'region', 'class_name',
                  'game_mode', 'season', 'records')

    def paginated_records(self, obj):
        page_size = 50
        paginator = Paginator(obj.records.filter(
            leaderboard_id=obj.id), page_size)
        page = self.context['request'].query_params.get('page') or 1

        records = paginator.page(page)
        serializer = RecordSerializer(records, many=True, read_only=True)

        return serializer.data
