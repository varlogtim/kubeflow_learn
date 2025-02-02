import os
import json
import requests

from typing import Tuple
from kfp.client import Client


def get_auth_session_cookies_from_user_pass(host: str, username: str, password: str) -> str:
    session = requests.Session()
    response = session.get(host)

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"login": username, "password": password}

    session.post(response.url, headers=headers, data=data)
    session_cookie = session.cookies.get_dict()["authservice_session"]

    return f"authservice_session={session_cookie}"


def get_credential_env_vars() -> Tuple[str, str, str, str]:
    # XXX This code might be unnecessary - Actually located similar env vars in the kfp.client.Client code.
    env_vars = {}
    env_var_keys = ["KFP_USER", "KFP_PASS", "KFP_HOST", "KFP_NAMESPACE"]
    for env_var_key in env_var_keys:
        env_vars[env_var_key] = os.environ.get(env_var_key)
        if env_vars[env_var_key] is None:
            raise RuntimeError(f"Could not find '${env_var_key}' environment variable which is required.")
    # XXX Maybe check the format of KFP_HOST, e.g., http://localhost:8080
    return env_vars["KFP_HOST"], env_vars["KFP_USER"], env_vars["KFP_PASS"], env_vars["KFP_NAMESPACE"]


def get_kfp_client_from_env() -> Client:
    host, username, password, namespace = get_credential_env_vars()
    session_cookies = get_auth_session_cookies_from_user_pass(host, username, password)

    return Client(host=f"{host}/pipeline", namespace=namespace, cookies=f"{session_cookies}")



# XXX If these functions work, encapsulate with an object
def get_kfp_client_context() -> dict:
    class Dummy:
        pass
    dummy = Dummy()
    Client._load_context_setting_or_default(dummy)
    return dummy._context_setting

def set_kfp_client_context(context: dict) -> None:
    if not os.path.exists(os.path.dirname(Client._LOCAL_KFP_CONTEXT)):
        os.makedirs(os.path.dirname(Client._LOCAL_KFP_CONTEXT))
    with open(Client._LOCAL_KFP_CONTEXT, "w") as f:
        json.dump(context, f)

def set_auth_session_cookies_in_context_from_env() -> None:
    host, username, password, namespace = get_credential_env_vars()
    session_cookies = get_auth_session_cookies_from_user_pass(host, username, password)

    context = get_kfp_client_context()
    context["client_authentication_cookie"] = session_cookies

    set_kfp_client_context(context)



