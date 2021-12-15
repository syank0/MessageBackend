# MessageBackend

A simple backend service for messages, using `Flask`, `jwt` for authentication and `sqlite3` for DB, and deployed with Heroku.

# API

## User related
+ `POST /register` expects a json with `username` and `password`, both strings. Returns the user if successful.
+ `POST /login` expects a json with `username` and `password`, both strings. Returns a token if successful.

## Message related
All of these require an 'Authorized' header with the token from the login.
+ `POST /api/post/message` expects a json with `receiver`, `message` and `subject`, all strings. Returns 200 on success.
+ `GET /api/get/messages` returns all messages the user received on success.
+ `GET /api/get/message/<id>`, returns a single message a user received by `id` on success.
+ `POST /api/delete/<id>`, exptects an `id` of message to delete as sender or as receiver. Returns 200 on success.
