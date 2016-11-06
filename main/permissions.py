from main.models import UserProfile


def has_student_permissions(user):
    user_profile = UserProfile.objects.get(user=user)
    if user_profile.is_student_user():
        return True
    else:
        return False


def has_tutor_permissions(user):
    user_profile = UserProfile.objects.get(user=user)
    if user_profile.is_tutor_user():
        return True
    else:
        return False
