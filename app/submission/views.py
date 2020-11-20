# Create your views here.
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from submission.models import RunSubmission
from submission.permissions import IsRunInTime, IsRunSelf
from submission.serializers import RunSubmissionSerializer


class Run(CreateAPIView):
    serializer_class = RunSubmissionSerializer
    permission_classes = [IsRunInTime]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class CheckRunStatus(RetrieveAPIView):
    serializer_class = RunSubmissionSerializer
    lookup_url_kwarg = 'id'
    queryset = RunSubmission.objects.all()
    permission_classes = [IsRunInTime, IsRunSelf]
