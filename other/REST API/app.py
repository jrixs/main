from flask import Flask, jsonify, request

app = Flask(__name__)
client = app.test_client()

tutorials = [
    {
        'id': 1,
        'test': 'vars1',
        'description': 'text1'
    },
    {
        'id': 2,
        'test': 'vars2',
        'description': 'text2'
    },
]

@app.route('/tutorial', methods=['GET'])
def get_list():
    return jsonify(tutorials)

@app.route('/tutorial', methods=['POST'])
def update_list():
    new_one = request.json
    tutorials.append(new_one)
    return jsonify(tutorials)

@app.route('/tutorial/<int:tutorial_id>', methods=['PUT'])
def update_tutorials(tutorial_id):
    item = next((x for x in tutorials if x['id'] == tutorial_id),None)
    params = request.json
    if not item:
        return {'message': 'No tutorials ID'}, 400
    item.update(params)
    return item

@app.route('/tutorial/<int:tutorial_id>', methods=['DELETE'])
def delete_tutorials(tutorial_id):
    idx, _ = next((x for x in enumerate(tutorials)
                   if x[1]['id'] == tutorial_id), (None, None))
    tutorials.pop(idx)
    return '', 204


if __name__ == '__main__':
    app.debug = True
    app.run(host='192.168.88.253', port=5050)