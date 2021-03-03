from rest_framework.throttling import UserRateThrottle


class RunThrottle(UserRateThrottle):
    scope = "run"


class RunRCThrottle(UserRateThrottle):
    scope = "run_rc"


class SubmitThrottle(UserRateThrottle):
    scope = "submit"
