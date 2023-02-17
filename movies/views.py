from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters import rest_framework as filters
from .models import Movie,Rating, Report
from .serializers import MovieSerializer,ReviewSerializer, ReportSerializer
from .pagination import CustomPagination
from .permissions import IsOwnerOrReadOnly, IsSuperUser, IsInappropriateOrAuthorOnly
from .filters import MovieFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

# Removes permissions from views


class ListCreateMovieAPIView(ListCreateAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.filter(is_inappropriate=False)
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)


    def perform_create(self, serializer):
        # Assign the user who created the movie
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, IsInappropriateOrAuthorOnly)
    authentication_classes = (JWTAuthentication,)


class ListCreateReviewAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)



class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JWTAuthentication,)


class CreateReportAPIView(CreateAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = (IsAuthenticated)
    authentication_classes = (JWTAuthentication,)

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

class ListReportAPIView(ListAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = (IsAuthenticated, IsSuperUser)
    authentication_classes = (JWTAuthentication,)


class RetrieveUpdateDestroyReportAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    queryset = Report.objects.all()
    permission_classes = (IsAuthenticated, IsSuperUser)
    authentication_classes = (JWTAuthentication,)