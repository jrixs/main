from app import app, client

#GET
res = client.get('http://192.168.88.253:5050/tutorial')
print(res.status_code)
print(res.get_json())

#POST
res = client.post('http://192.168.88.253:5050/tutorial', json={'test': 'vars3', 'description': 'text3'})
print(res.status_code)
print(res.get_json())

#PUT
res = client.put('http://192.168.88.253:5050/tutorial/2', json={'description': 'text30'})
print(res.status_code)
print(res.get_json())

#DELETE
res = client.delete('http://192.168.88.253:5050/tutorial/1')
print('delete')
print(res.status_code)
