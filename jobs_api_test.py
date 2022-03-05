from requests import get

print(get('http://localhost:8080/api/jobs').json())

print(get('http://localhost:8080/api/jobs/1').json())

print(get('http://localhost:8080/api/jobs/8989').json())

print(get('http://localhost:8080/api/jobs/rt').json())

