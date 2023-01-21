from website.models.user import User
import json

# jen pro moje info:
dostupna_omezeni = ["user", "admin", "editing_bugs_allowed", "editing_logs_allowed", "editing_users_allowed", "editing_admins_allowed", "stanovit_terminy_allowed", "prepinani_fazi_allowed", "velitel_odbornosti", "velitel_odbornosti_biolog", "velitel_odbornosti_konstrukter", "velitel_odbornosti_fyzik", "velitel_odbornosti_inzenyr","velitel_odbornosti_popularizator", "editing_pohovory"]

def get_access_rights(userobj: User) -> list:
    role = []
    if userobj.is_authenticated:
        role.extend(json.loads(userobj.role))
        # prihlasen - proto, aby se mohli logoutnout i user i admin
        role.append("prihlasen")
        # dalsi vyjimka - pokud jeste neni overenej, tak to vrati role tak, aby videl jen ucet a tam vyzvu k overeni
        if userobj.confirmed:
            role.append("confirmed")
    return role