from website.models.user import User
from typing import List
from website.paths.paths import user_data_folder_path

def user_filter(kriteria: dict) -> List[User]:
    print(kriteria)
    users = User.query.all()
    if kriteria["odbornost"] == "jakakoli":
        pass
    else:
        users = filter(lambda x: x.odbornost in kriteria["odbornost"], users)
    
    if kriteria["postup"] == "jakykoli":
        pass
    else:
        users = filter(lambda x: x.progress in kriteria["postup"], users)
    
    if kriteria["udaj"] == "motivak":
        path = user_data_folder_path()
    if kriteria["udaj"] == "prace":
        pass
    if kriteria["udaj"] == "profilovka":
        pass

    return users