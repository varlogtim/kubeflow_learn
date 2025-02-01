import os
import requests

from kfp.client import Client


def get_kfp_client_from_env() -> Client:
    # XXX This code might be unnecessary
    env_vars = {}
    env_var_keys = ["KFP_USER", "KFP_PASS", "KFP_HOST", "KFP_NAMESPACE"]
    for env_var_key in env_var_keys:
        env_vars[env_var_key] = os.environ.get(env_var_key)
        if env_vars[env_var_key] is None:
            raise RuntimeError(f"Could not find '${env_var_key}' environment variable which is required.")

    # XXX Maybe check the format of KFP_HOST, e.g., http://localhost:8080

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "login": env_vars["KFP_USER"],
        "password": env_vars["KFP_PASS"]
    }

    session = requests.Session()
    response = session.get(env_vars["KFP_HOST"])

    session.post(response.url, headers=headers, data=data)
    session_cookie = session.cookies.get_dict()["authservice_session"]

    return Client(
        host=f"{env_vars['KFP_HOST']}/pipeline",
        namespace=env_vars["KFP_NAMESPACE"],
        cookies=f"authservice_session={session_cookie}",
    )

