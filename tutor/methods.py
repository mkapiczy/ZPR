from main.models import UserProfile
from tutor.models import TutorUser


def getTutorUserFromRequest(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return TutorUser.objects.get(profile_id=user_profile.id)