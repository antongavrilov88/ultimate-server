from functools import wraps


def admin_access_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        current_user = kwargs['current_user']
        if not current_user.is_admin:
            return {"message": 'Forbidden'}, 403
        return f(*args, **kwargs)

    return decorator
