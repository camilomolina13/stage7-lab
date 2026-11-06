#!/usr/bin/env bash
# Uso: bash compare.sh   (Flask en :5000 y Django en :8000 deben estar corriendo)

fetch() {  # puerto método ruta [body]
  local out code body
  out=$(curl -s -w '\n%{http_code}' -X "$2" "localhost:$1$3" -H "Content-Type: application/json" ${4:+-d "$4"})
  code=${out##*$'\n'}
  body=${out%$'\n'*}
  echo "$code"
  [ -n "$body" ] && echo "$body" | python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin), sort_keys=True))"
}

check() {  # método ruta [body]
  local flask django
  flask=$(fetch 5000 "$@")
  django=$(fetch 8000 "$@")
  if [ "$flask" == "$django" ]; then
    echo "OK    $1 $2 $3"
  else
    echo "DIFF  $1 $2 $3"; diff <(echo "$flask") <(echo "$django")
  fi
}

check POST /api/projects '{"name":"  "}'
check POST /api/projects '[1,2]'
check POST /api/projects '{"name":'
check POST /api/projects '{"name":123}'
check POST /api/tasks '{"project_id":999999,"status":"X","due_date":"15/11/2026"}'
check POST /api/tasks '{"project_id":"1","title":"x"}'
check POST /api/tasks '{"project_id":null,"title":null,"priority":5}'
check GET  "/api/tasks?project_id=abc"
check GET  /api/tasks/999999
check GET  /api/projects/abc
check GET  /api/nada
check PATCH /api/tasks/1
check PUT  /api/projects/999999 '{"name":""}'
check DELETE /api/tasks/999999