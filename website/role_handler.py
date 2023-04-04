from website.models.user import User
from flask_login import current_user
import json

def get_access_rights(userobj: User = current_user) -> list:
    role = []
    if userobj.is_authenticated:
        role.extend(json.loads(userobj.role))
        # prihlasen - proto, aby se mohli logoutnout i user i admin
        role.append("prihlasen")
        # dalsi vyjimka - pokud jeste neni overenej, tak to vrati role tak, aby videl jen ucet a tam vyzvu k overeni
        if userobj.confirmed:
            role.append("confirmed")
    return role