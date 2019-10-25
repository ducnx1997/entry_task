from api.models import User


def get_user(username=None, user_id=None, email=None):
    user = User.objects

    if user_id:
        user = user.filter(id=user_id)

    if username:
        user = user.filter(username=username)

    if email:
        email = user.filter(email=email)


