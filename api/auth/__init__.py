import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from api.config import settings

basic_auth = HTTPBasic(auto_error=False)


def authent(
    credentials: HTTPBasicCredentials = Depends(basic_auth),
):
    if not credentials:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    if check_basic_auth_creds(credentials):
        return True

    raise HTTPException(status_code=403, detail="Invalid username/password")


def check_basic_auth_creds(
    credentials: HTTPBasicCredentials,
):
    correct_username = secrets.compare_digest(
        credentials.username, settings.API_USERNAME
    )
    correct_password = secrets.compare_digest(
        credentials.password, settings.API_PASSWORD
    )

    return correct_username and correct_password
