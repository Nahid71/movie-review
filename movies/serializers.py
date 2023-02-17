from rest_framework import serializers
from .models import Movie,Rating, Report
from django.contrib.auth.models import User

class MovieSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='username')

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'year', 'creator', 'avg_rating')

    def to_representation(self, instance):
        data = super(MovieSerializer, self).to_representation(instance)
        # By default inappropriate is false
        data["inappropriate"] = False
        for report in instance.r_movie.all():
            if report.state == "resolved":
                data["inappropriate"] = True
                break
        return data

class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'movies')


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(many=False,queryset=Movie.objects.all())
    reviewer = serializers.ReadOnlyField(source='username')

    class Meta:
        model = Rating
        fields = ('id','movie','score','reviewer')

    def create(self, validated_data):
        if validated_data['score'] < 1 or validated_data['score'] > 5:
            raise serializers.ValidationError('Score needs to between 1 to 5')
        review = super(ReviewSerializer, self).create(validated_data)
        review.movie.update_avg_rating()
        return review
    
    def update(self, instance, validated_data):
        if 'score' in validated_data:
            if validated_data['score'] < 1 or validated_data['score'] > 5:
                raise serializers.ValidationError('Score needs to between 1 to 5')
        review = super(ReviewSerializer,self).update(instance, validated_data)
        review.movie.update_avg_rating()
        return review

    def delete(self, *args, **kwargs):
        review = self.instance
        review.deleted = True
        review.save()
        review.movie.update_avg_rating()

class ReportSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(many=False,queryset=Movie.objects.all())
    reporter = serializers.ReadOnlyField(source='username')

    class Meta:
        model = Report
        fields = ('id','movie','state','reporter')
    
    def update(self, instance, validated_data):
        if 'state' in validated_data:
            # fetch the movie object
            movie_obj = instance.movie
            if validated_data['state'] == 'resolved':
                # update all the reports object to 'resolve' state, because one resolved mean all resolved
                movie_obj.r_movie.all().update(state='resolved')
                movie_obj.is_inappropriate = True
            else:
                movie_obj.r_movie.all().update(state=validated_data['state'])
                movie_obj.is_inappropriate = False
            movie_obj.save()
        repost = super(ReportSerializer,self).update(instance, validated_data)
        return repost