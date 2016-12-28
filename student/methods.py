from main.models import UserProfile
from student.models import StudentUser


def get_student_user_from_request(request):
    user_profile = UserProfile.objects.get(user=request.user)
    student = StudentUser.objects.get(profile_id=user_profile.id)
    return student