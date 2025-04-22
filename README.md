# web_server
Building a web server using only base python and rendering a few html pages with login authentication.
<fieldset>Note: run all .py files from the <code>py_files</code> directory</fieldset>

## Steps
1. Clone this repo onto a linux machine/subsystem.
2. Set up a mysql/sqlite database with a `users` table per the create_users.sql file.
3. Set up python venv with packages listed in `requirements.txt` (run all python files from this venv)
4. Add `.env` file at root of clone directory with `MINI_SOCIAL_SALT`, `MYSQL_USER`, and `MYSQL_PW` variables set appropriately.
5. Modify `DATABASE_NAME` variable in py_files/add_user.py and py_files/runserver.py to the database name you use for your table.
6. Run py_files/add_user.py to add users to the database, follow console prompts.
7. Run py_files/runserver.py with `-h` flag to see the argument options.
8. Run `runserver.py` \<time to run server for\> \<unit of time\> \<number of threads to use for server\> e.g. runserver.py 2 min 20
9. Enter `127.0.0.1` in a browser after server is listening on port 80. Attempt login based on users you entered.

## Notes
- This repo is meant to show how a simple webserver works from the lowest level abstraction, `Berkley Sockets`.
- The server is managed with python, in a production setting `Gunicorn` is the production web server backend.
- Read through the code base to see the internals of what a simple web server does to render html content to a user.
- Modify `py_files/data/conn.py` if you would like to use a db dialect other than mysql or sqlite.

