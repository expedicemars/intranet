from website.models.user import User
import json

dostupna_omezeni = ["user", "admin", "editing_bugs_allowed", "editing_logs_allowed", "editing_users_allowed", "editing_admins_allowed", "stanovit_terminy_allowed", "prepinani_fazi_allowed"]

def get_access_rights(userobj: User) -> list:
    if userobj.is_authenticated:
        role = json.loads(userobj.role)
        # superadmin přebíjí vše: to dodává smysl tomu skriptu, kterej může vždy vytvořit superadmina, i když se správa stránek předá
        if "superadmin" in role:
            return dostupna_omezeni
        # dalsi vyjimka - pokud jeste neni overenej, tak to vrati role tak, aby videl jen ucet a tam vyzvu k overeni
        if not userobj.confirmed:
            role.append("not_confirmed")
            return role
        else:
            return role

    else:
        return []