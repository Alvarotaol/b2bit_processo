from rest_framework.throttling import UserRateThrottle

class SignupRateThrottle(UserRateThrottle):
    scope = 'signup'
