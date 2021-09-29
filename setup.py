import setuptools

VERSION = "0.0.5"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AuthX",
    version=VERSION,
    author="Yasser Tahiri",
    author_email="yasserth19@gmail.com",
    description="Ready to use and customizable Authentications and Oauth2 management for FastAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yezz123/AuthX",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "fastapi==0.61.1",
        "PyJWT==1.7.1",
        "cryptography==3.1.1",
        "httpx==0.16.1",
        "aioredis==1.3.1",
        "passlib==1.7.4",
        "itsdangerous==1.1.0",
        "bcrypt==3.2.0",
        "email-validator==1.1.1",
        "motor==2.3.0",
        "aiosmtplib==1.1.4",
        "pydantic==1.8.2",
    ],
    extras_require={"dev": ["requests == 2.25.1" "uvicorn"]},
)
