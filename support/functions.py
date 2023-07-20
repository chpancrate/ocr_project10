from support.models import Contributor


def is_contributor(user, project):

    try:
        Contributor.objects.get(project=project,
                                user=user)
        return True
    except Contributor.DoesNotExist:
        return False