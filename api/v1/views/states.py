from flask import Flask, make_response, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State
# index

@app_views.route('/states', methods=['GET', 'POST'])
def all_states():
    if request.method == 'GET':
        return jsonify([state.to_dict()
                        for state in storage.all('State').values()])
    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if not 'name' in request.json:
            abort(400, 'Missing name')
        new = request.get_json()
        new_State = State()
        new_State.name = new
        new_State.save()
        return make_response(jsonify(new_State.to_dict()), 200)

@app_views.route('/states/<state_id>', methods=['GET', 'DELETE','PUT'])
def state(state_id):

    state = storage.get('State', state_id)

    if not state:
        abort(404)

    if request.method == 'GET':
        return make_response(jsonify(state.to_dict()), 200)

    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if not key in ["id", "created_at", "updated_at"]:
                setattr(state, key, value)
        state.save()
        return make_response(jsonify(state.to_dict()), 200)