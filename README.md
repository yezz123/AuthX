# AuthenticationX 💫

![authx](https://user-images.githubusercontent.com/52716203/136962014-280d82b0-0640-4ee5-9a11-b451b338f6d8.png)

<p align="center">
    <em>Ready-to-use and customizable Authentications and Oauth2 management for FastAPI ⚡</em>
</p>

[![Test](https://github.com/yezz123/authx/actions/workflows/build.yml/badge.svg)](https://github.com/yezz123/authx/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/yezz123/AuthX/branch/main/graph/badge.svg?token=3j5znCNzDp)](https://codecov.io/gh/yezz123/AuthX)
[![PyPI version](https://badge.fury.io/py/authx.svg)](https://badge.fury.io/py/authx)
[![Downloads](https://pepy.tech/badge/authx)](https://pepy.tech/project/authx)
[![Language](https://img.shields.io/badge/Language-Python-green?style)](https://github.com/yezz123)
[![framework](https://img.shields.io/badge/Framework-FastAPI-blue?style)](https://fastapi.tiangolo.com/)
[![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flatcolor=BC4E99)](https://github.com/yezz123/AuthX)
[![Pypi](https://img.shields.io/pypi/pyversions/AuthX.svg?color=%2334D058)](https://pypi.org/project/AuthX)

---

**Source Code**: <https://github.com/yezz123/AuthX>

**Documentation**: <https://authx.yezz.codes/>

---

Add a Fully registration and authentication or authorization system to your [FastAPI](https://fastapi.tiangolo.com/) project. **AuthX** is designed to be as customizable and adaptable as possible.

__Note__: This is a **beta** version of AuthX.

## Features 🔧

- Support Python 3.8+.
- Extensible base user model.
- Ready-to-use register, login, reset password and verify e-mail routes.
- Ready-to-use Social login and Oauth2 routes. (now with Google, Facebook)
    - Soon with Microsoft, Twitter, Github, etc.
    - Ready-to-use social OAuth2 login flow
- Dependency callable to inject current user in route
- Pluggable password validation
    - Using Captcha Service.
- Using Email Service. (SMTP)
- Extensible Error Handling
- High level API to manage users, roles and permissions
- Using Redis as a session store & cache.
- Customizable database backend:
    - MongoDB async backend included thanks to [mongodb/motor](https://github.com/mongodb/motor)
- Multiple customizable authentication backend:
    - JWT authentication backend included
    - Soon to be included Cookie authentication backend
- Full OpenAPI schema support, even with several authentication backend.
- Provide a Docstring for each class and function.
- Middleware Support for Oauth2 using `Authlib` and Starlette.

__Note:__ Check [Release Notes](https://authx.yezz.codes/release/).

## Project using 🚀

```python
from fastapi import FastAPI
from authx import Authentication

app = FastAPI()
auth = Authentication()

# Define your routes here
app.include_router(auth.auth_router, prefix="/api/users")
app.include_router(auth.social_router, prefix="/auth")
app.include_router(auth.password_router, prefix="/api/users")
app.include_router(auth.admin_router, prefix="/api/users")
app.include_router(auth.search_router, prefix="/api/users")

```

### Startup 🏁

```python
from fastapi import FastAPI
from authx import Authentication
from authx.database import MongoDBBackend, RedisBackend

app = FastAPI()
auth = Authentication()

app.include_router(auth.auth_router, prefix="/api/users")
app.include_router(auth.social_router, prefix="/auth")
app.include_router(auth.password_router, prefix="/api/users")
app.include_router(auth.admin_router, prefix="/api/users")
app.include_router(auth.search_router, prefix="/api/users")

# Set MongoDB and Redis Cache
auth.set_cache(RedisBackend) # aioredis client
auth.set_database(MongoDBBackend) # motor client
```

### Dependency injections 📦

```python
from fastapi import FastAPI,APIRouter, Depends
from authx import User, Authentication
from authx.database import MongoDBBackend, RedisBackend

app = FastAPI()
auth = Authentication()
router = APIRouter()


app.include_router(auth.auth_router, prefix="/api/users")
app.include_router(auth.social_router, prefix="/auth")
app.include_router(auth.password_router, prefix="/api/users")
app.include_router(auth.admin_router, prefix="/api/users")
app.include_router(auth.search_router, prefix="/api/users")

# Set MongoDB and Redis Cache
auth.set_cache(RedisBackend) # aioredis client
auth.set_database(MongoDBBackend) # motor client

# Set Anonymous User
@router.get("/anonym")
def anonym_test(user: User = Depends(auth.get_user)):
    pass

# Set Authenticated User
@router.get("/user")
def user_test(user: User = Depends(auth.get_authenticated_user)):
    pass

# Set Admin User
@router.get("/admin", dependencies=[Depends(auth.admin_required)])
def admin_test():
    pass

```

### Dependency injections only 📦

```python
from authx import authx
from authx.database import RedisBackend

auth = authx(#Provide Config)

# startup
auth.set_cache(RedisBackend) # aioredis
```

## Development 🚧

### Setup environment 📦

You should create a virtual environment and activate it:

```bash
python -m venv venv/
```

```bash
source venv/bin/activate
```

And then install the development dependencies:

```bash
pip install -r requirements.dev.txt
```

### Run tests 🌝

I use Pytest to run the tests, you can run this by using a shortcut command in the `Makefile`:

```bash
make test
```

### Format the code 🍂

Execute the following command to apply `pre-commit` formatting:

```bash
make lint
```

## Contributors and sponsors ✨☕️

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-6-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="http://yezz.me"><img src="https://avatars.githubusercontent.com/u/52716203?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Yasser Tahiri</b></sub></a><br /><a href="https://github.com/yezz123/authx/commits?author=yezz123" title="Code">💻</a> <a href="https://github.com/yezz123/authx/commits?author=yezz123" title="Documentation">📖</a> <a href="#maintenance-yezz123" title="Maintenance">🚧</a> <a href="#infra-yezz123" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
    <td align="center"><a href="https://soubai.me"><img src="https://avatars.githubusercontent.com/u/11523791?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Abderrahim SOUBAI-ELIDRISI</b></sub></a><br /><a href="https://github.com/yezz123/authx/pulls?q=is%3Apr+reviewed-by%3AAbderrahimSoubaiElidrissi" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/yezz123/authx/commits?author=AbderrahimSoubaiElidrissi" title="Documentation">📖</a></td>
    <td align="center"><a href="https://smakosh.com"><img src="https://avatars.githubusercontent.com/u/20082141?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ismail Ghallou </b></sub></a><br /><a href="https://github.com/yezz123/authx/commits?author=smakosh" title="Code">💻</a> <a href="#security-smakosh" title="Security">🛡️</a></td>
    <td align="center"><a href="https://talentuno.com/en/matchmakers"><img src="https://talentuno.com/assets/img/talentuno/mm/mm-letsdoit_num1.png?s=100" width="100px;" alt=""/><br /><sub><b>talentuno LLC</b></sub></a><br /><a href="#financial-talentuno" title="Financial">💵</a></td>
    <td align="center"><a href="https://www.stryker.com/us/en/index.html"><img src="https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_256,w_256,f_auto,q_auto:eco,dpr_1/v1492757324/sdovorqhcnnkgybhf05h.jpg?s=100" width="100px;" alt=""/><br /><sub><b>Cactus LLC</b></sub></a><br /><a href="#financial-Cactus" title="Financial">💵</a></td>
    <td align="center"><a href="https://github.com/MojixCoder"><img src="https://avatars.githubusercontent.com/u/76670309?v=4?s=100" width="100px;" alt=""/><br /><sub><b>MojixCoder</b></sub></a><br /><a href="https://github.com/yezz123/authx/commits?author=MojixCoder" title="Code">💻</a> <a href="https://github.com/yezz123/authx/issues?q=author%3AMojixCoder" title="Bug reports">🐛</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

<a href="https://www.producthunt.com/posts/authx?utm_source=badge-featured&utm_medium=badge&utm_souce=badge-authx" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=318189&theme=dark" alt="AuthX - A FastAPI package for Auth made by a human not an AI | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>
<a href="https://www.buymeacoffee.com/tahiri" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

## License 📝

This project is licensed under the terms of the MIT License.
