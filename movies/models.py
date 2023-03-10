from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255,unique=True)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('auth.User', related_name='films', on_delete=models.CASCADE)
    avg_rating = models.FloatField(null=True,blank=True)
    is_inappropriate = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def update_avg_rating(self):
        all_movies =  self.movie.all()
        self.avg_rating = sum(rating.score for rating in all_movies) / all_movies.count()
        self.updated_at = self.updated_at
        self.save()

class Rating(models.Model):
    movie = models.ForeignKey(Movie,related_name='movie',on_delete=models.CASCADE)
    reviewer = models.ForeignKey('auth.User', related_name='reviewer', on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

class Report(models.Model):
    STATE_CHOICES = (
        ('unresolved', 'unresolved'),
        ('resolved', 'resolved'),
        ('reject', 'rejected'),
    )
    movie = models.ForeignKey(Movie,related_name='r_movie',on_delete=models.CASCADE)
    reporter = models.ForeignKey('auth.User', related_name='repoter', on_delete=models.CASCADE)
    state = models.CharField(max_length=30, choices=STATE_CHOICES, default="unresolved")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
