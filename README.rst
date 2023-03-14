Config Required
----------
- Install ``Python >= 3.8``: `Python <https://www.python.org/downloads/release/python-382/>`_:
- Install ``Oracle Client``: `cx_Oracle <https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html#installing-cx-oracle-on-linux>`_:

Quickstart
----------

First, Setup venv python `Document Setup <https://docs.python.org/3.9/library/venv.html>`_: ::

    python -m venv venv

    Windows:
    - Cmd: .\venv\Scripts\activate
    Linux:
    - Terminal: source venv/bin/activate

Then run the following commands to bootstrap your environment with ``PIP``: ::

    Windows:
    - cmd: python -m pip install -r requirements/local_windows.txt
    Linux:
    - Terminal: sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev
    - Terminal: pip install -r requirements/local_debian.txt

Then create ``.env`` file (or copy and modify ``.env.example.yaml``) in project root and set environment variables for application: ::

    Windows:
    - cmd: copy env.example.yaml .env
    Linux:
    - Terminal: cp env.example.yaml .env

Then Install ``pre-commit``: ::

    Windows:
    - cmd: pre-commit install

    Linux:
    - Terminal: pre-commit install


To run the web application in debug use::

    Develop:
    - uvicorn app.main:app --port {port} --reload
    Deploy:
    - gunicorn app.main:app -k uvicorn.workers.UvicornWorker

    Lưu ý:
    - Config worker, port, host trong file gunicorn.conf.py




Project structure
-----------------

Files related to application are in the ``app`` directories.
Application parts are::

    .
    ├── app
    │   ├── api
    │   │   └── v1
    │   │       ├── controllers
    │   │       ├── dependencies
    │   │       ├── endpoints
    │   │       └── schemas
    │   ├── repositories
    │   ├── settings
    │   ├── third_party
    │   │   ├── oracle
    │   │   │   └── models
    │   │   └── services
    │   └── utils
    ├── backup
    │   └── oracle
    └── requirements

-----------------
