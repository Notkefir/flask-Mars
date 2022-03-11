from requests import get, post, delete

print(get('http://localhost:8080/api/v2/users').json())

print(get('http://localhost:8080/api/v2/users/1').json())

print(get('http://localhost:8080/api/v2/users/787').json())

print(post('http://localhost:8080/api/v2/users',
           json={'surname': 'Заголовок',
                 'name': 'Текст новости',
                 'age': 1,
                 'position': 'Soccer',
                 'speciality': 'Cooller',
                 'address': 'Moon',
                 'email': 'sss@aa.aa',
                 'hashed_password': 'qwer'}).json())

print(post('http://localhost:8080/api/v2/users',
           json={'surname': 'Заголовок', }).json())

print(delete('http://localhost:8080/api/v2/users/787').json())

print(delete('http://localhost:8080/api/v2/users/1').json())
