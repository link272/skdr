BUILD

docker-compose up

TEST FRONT

http://localhost:8000/


TEST API

curl -H 'Content-Type: application/json; indent=4' -X POST -u test:test -d '{"url":"http://www.google.com"}' http://localhost:8000/api/webpages/
