service supervisor restart
supervisorctl reread
supervisorctl add all
while true; do sleep 10; done
