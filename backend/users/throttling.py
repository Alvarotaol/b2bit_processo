from rest_framework.throttling import UserRateThrottle

class SignupRateThrottle(UserRateThrottle):
    scope = 'signup'

class LoginRateThrottle(UserRateThrottle):
    scope = 'login'