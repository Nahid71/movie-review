from rest_framework import serializers
from .models import Movie,Rating
from django.contrib.auth.models import User

class MovieSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='username')

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'year', 'creator', 'avg_rating')

    def update(self, instance, validated_data):
        if self.context['request'].user != instance.creator:
            raise serializers.ValidationError('Only author can edit the movie')
        movie = super(MovieSerializer,self).update(instance, validated_data)
        return movie
    
    def delete(self, *args, **kwargs):
        instance = self.instance
        if self.context['request'].user != instance.creator:
            raise serializers.ValidationError('Only author can delete the movie')
        instance.deleted = True
        instance.save()

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
        if self.context['request'].user != instance.reviewer:
            raise serializers.ValidationError('Only author can edit the rating')
        if validated_data['score'] < 1 or validated_data['score'] > 5:
            raise serializers.ValidationError('Score needs to between 1 to 5')
        review = super(ReviewSerializer,self).update(instance, validated_data)
        review.movie.update_avg_rating()
        return review
    
    def delete(self, *args, **kwargs):
        instance = self.instance
        if self.context['request'].user != instance.reviewer:
            raise serializers.ValidationError('Only author can delete the rating')
        instance.deleted = True
        instance.save()
        instance.movie.update_avg_rating()