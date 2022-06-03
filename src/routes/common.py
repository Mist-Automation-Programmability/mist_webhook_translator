
from mwtt import Console

console = Console("api_common")

def extract_json(request):
    if not hasattr(request, "data"):
        return False, "No data"
    elif not request.is_json:
        return False, "Malformed data"
    else:
        return True, request.get_json()

def check_privilege(session, org_id):
    for privilege in session["privileges"]:
            if privilege.get("scope") == "org" and privilege.get("role") == "admin" and org_id == privilege["org_id"]:
                console.debug("user authorized")
                return privilege
    console.warning("user not authorized")
    return None
