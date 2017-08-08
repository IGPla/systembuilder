#basicdjango template

basicdjango template offers 2 environments: dev and prod. It will deploy a basic django project, initialized with a database (postgres) and a running server (depending on the environment, server will be the default runserver on dev and nginx+uwsgi in prod)