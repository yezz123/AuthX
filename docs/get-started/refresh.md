# Refreshing Tokens

JWTs come with a strict `exp` (Expiration Time), which means that a long session might lead to multiple logouts and `401 Authentication` errors. To mitigate such behavior, refresh tokens are employed to facilitate the generation of additional access tokens without requiring the user to log in again.

## Implicit refresh with Cookies

The most common way to refresh tokens is by using cookies. When the access token expires, the client sends a request to the server with the refresh token stored in a cookie. The server then generates a new access token and sends it back to the client in the response.

!!! warning
    Cookies are not supported in all environments, such as mobile applications, SDKs, or APIs. In such cases, you may need to implement an explicit refresh mechanism.

!!! note
    Work in progress: This feature need to be documented.

## Explicit Refresh

In cases where implicit refresh isn't feasible—such as in mobile applications, SDKs, or APIs—you may need to explicitly declare the refresh logic in your application.

To implement an explicit refresh mechanism, you need to create a new route that accepts the refresh token and returns a new access token. This route should be protected by the `refresh_token_required` dependency, which will verify the refresh token and extract the payload.

!!! note
    The refresh token should be stored securely on the client side, and the route should be protected by HTTPS to prevent tampering.

```python
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
from authx import AuthX, AuthXConfig, TokenPayload

# Create an AuthX configuration
auth_config = AuthXConfig()
auth_config.JWT_ALGORITHM = 'HS256'
auth_config.JWT_SECRET_KEY = 'SECRET_KEY'
auth_config.JWT_TOKEN_LOCATION = ['headers']


app = FastAPI()
security = AuthX(auth_config)

class LoginForm(BaseModel):
    username: str
    password: str

@app.post('/login')
def login(data: LoginForm):
    if data.username == "test" and data.password == "test":
        access_token = security.create_access_token(data.username)
        refresh_token = security.create_refresh_token(data.username)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    raise HTTPException(401, "Bad username/password")


@app.post('/refresh')
def refresh(
    refresh_payload: TokenPayload = Depends(security.refresh_token_required)
):
    access_token = security.create_access_token(refresh_payload.sub)
    return {"access_token": access_token}


@app.get('/protected', dependencies=[Depends(security.access_token_required)])
def protected():
    return "You have access to this protected resource"
```

In this example, the `/refresh` route only searches for a valid refresh token in the request. Once verified, it generates a new access token to extend the session.

This example provides a basic implementation of an explicit refresh mechanism. In a production scenario, you might want to retrieve the current access token to revoke it, thereby avoiding the generation of an infinite number of valid access tokens.

=== "1. Login"

    ```sh
    # To obtain a token, we log in
    $ curl -s -X POST --json '{"username":"test", "password":"test"}' http://0.0.0.0:8000/login
    {"access_token": $TOKEN, "refresh_token": $REFRESH_TOKEN}
    ```
=== "2. Performing Sensitive Operations"

    ```sh
    # We request access to the protected route with the token
    $ curl -s --oauth2-bearer $TOKEN http://0.0.0.0:8000/protected
    "You have access to this protected resource"
    ```
=== "3. Refreshing Access Token"

    ```sh
    # To obtain a new access token, we refresh it
    $ curl -s --oauth2-bearer $REFRESH_TOKEN http://0.0.0.0:8000/refresh
    {"access_token": $NEW_TOKEN}
    ```

As demonstrated in the final step, the refreshing mechanism enables the acquisition of new tokens without the need for re-authentication.
