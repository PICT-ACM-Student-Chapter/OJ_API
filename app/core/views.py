import datetime
import os

import requests

from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import HttpResponseRedirect
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from contest.models import Contest
from contest.serializers import UserContestSerializer
from core.models import Language, UserContest
from core.serializers import LanguageSerializer
from sentry_sdk import capture_message
from rest_framework_simplejwt.tokens import RefreshToken


class LanguageList(generics.ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    authentication_classes = ()
    pagination_class = None

    def get(self, request, *args, **kwargs):
        res = cache.get('languages')
        if not res:
            res = self.list(request, *args, **kwargs).data
            cache.set('languages', res, settings.CACHE_TTLS['LANGS'])
        return Response(data=res)


class UserContestRetrieve(generics.RetrieveAPIView):
    lookup_url_kwarg = 'id'
    serializer_class = UserContestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserContest.objects.filter(user_id=self.request.user)


class ServerTime(APIView):
    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        return Response({"time": now})


class Version(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(redirect_to='/swagger')


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(data={'error': 'invalid data'},
                            status=status.HTTP_400_BAD_REQUEST)

        # query to ems
        url = '{}/user/signin'.format(os.environ.get('EMS_API'))
        data = {
            'email': email,
            'password': password
        }
        res = requests.post(url, data=data)

        if res.status_code == status.HTTP_401_UNAUTHORIZED:
            return Response(data=res.json(),
                            status=status.HTTP_401_UNAUTHORIZED)

        # get user
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            user = User.objects.create_user(username=email,
                                            email=email, password=password)
            user.first_name = res.json().get('user').get('first_name')
            user.last_name = res.json().get('user').get('last_name')
            user.save()

        if res.status_code == status.HTTP_200_OK:
            token = res.json().get('token')
            # query my events
            url = '{}/user_events'.format(os.environ.get('EMS_API'))
            myevent_res = requests.get(url, headers={
                'Authorization': 'Bearer ' + token})

            if myevent_res.status_code == status.HTTP_401_UNAUTHORIZED:
                return Response(data=myevent_res.json(),
                                status=status.HTTP_401_UNAUTHORIZED)

            events = myevent_res.json()

            for event in events:
                try:
                    slot_id = event['slot_id']['_id']
                except TypeError:
                    slot_id = None

                if slot_id:
                    try:
                        contest = Contest.objects.get(ems_slot_id=slot_id)
                    except Contest.DoesNotExist:
                        capture_message(
                            "Contest not present for slot {}".format(slot_id),
                            level="error")
                        continue

                    # create user contest
                    uc, _ = UserContest.objects.get_or_create(
                        user_id=user, contest_id=contest)

            # create jwt token
            refresh = RefreshToken.for_user(user)

            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data=data, status=status.HTTP_200_OK)
