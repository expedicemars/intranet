from functools import wraps
from flask import abort
from flask_login import current_user
from website import role_handler


def require_role_on_current_user(role: str, user = current_user):
    """Můj pokus o napsání login_required decoratoru

    Args:
        role (str | list): tahle role se vyžaduje | jedna z rolí se vyžaduje
        user (_type_, optional): _description_. Defaults to current_user.
    """
    if type(role) == str:
        role = [role]
    def what_should_i_name_this(original_function):
        @wraps(original_function)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated:
                user_roles = role_handler.get_access_rights(user)
                for r_input in role:
                    if r_input in user_roles:
                        result = original_function(*args, **kwargs)
                        return result
            abort(401)
        return wrapper
    return what_should_i_name_this