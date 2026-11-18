from django.contrib.auth import get_user_model
from django.db.models.base import Model
from django.http.request import HttpRequest

User = get_user_model()


def get_user_reaction(request: HttpRequest, obj, _Model: Model, field_name: str):
    if not request:
        return ''
    user = request.user
    if not user.is_authenticated:
        return ''
    filter_kwargs = {
        'user': user,
        field_name: obj
    }
    instance = _Model.objects.filter(**filter_kwargs).first()
    if instance:
        return instance.reaction
    return ''
