
from database.models import Drink, db_search_drink_by_id
from database.models import db_create_new_drink
from needed_services import server_drink_response
from needed_services import server_drink_delete_response
from auth.auth import requires_auth
from flask import abort, request, json


def get_drinks():
    try:
        all_drinks = Drink.query.all()

        map_drinks_short = [d.short() for d in all_drinks]
        if not len(map_drinks_short):
            abort(404)
        return server_drink_response(
            success=True,
            drinks=map_drinks_short,
            code=200
        )
    except Exception:
        abort(500)


@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        all_drinks = Drink.query.all()

        map_drinks_long = [d.long() for d in all_drinks]

        return server_drink_response(
            success=True,
            drinks=map_drinks_long,
            code=200
        )
    except Exception:
        abort(500)


@requires_auth('post:drinks')
def create_drink(payload):
    try:
        body = request.get_json()

        new_drink = db_create_new_drink(
            title=body['title'],
            recipe=json.dumps(body['recipe'])
        )

        return server_drink_response(
            success=True,
            drinks=[new_drink.long()],
            code=200
        )
    except Exception:
        abort(400)


@requires_auth('patch:drinks')
def update_drink(payload, id):
    try:

        body = request.get_json()
        title = body.get('title')
        recipe = body.get('recipe')

        if not title or not recipe:
            abort(400)

        found_drink = db_search_drink_by_id(id)
        if not found_drink:
            abort(404)

        found_drink.title = title
        found_drink.recipe = json.dumps(body['recipe'])
        found_drink.update()
        return server_drink_response(
            success=True,
            drinks=[found_drink.long()],
            code=200
        )

    except Exception:
        abort(400)


@requires_auth('delete:drinks')
def delete_drink(payload, id):

    try:
        found_drink = db_search_drink_by_id(id)

        if not found_drink:
            abort(404)

        found_drink.delete()

        return server_drink_delete_response(
            success=True,
            id=id,
            code=200
        )
    except Exception:
        abort(400)


def create_controller(app):
    app.add_url_rule(
        '/drinks',
        'get_drinks',
        get_drinks,
        methods=['GET']
    )
    app.add_url_rule(
        '/drinks-detail', 
        'get_drinks_detail',
        get_drinks_detail,
        methods=['GET']
    )
    app.add_url_rule(
        '/drinks',
        'create_drink',
        create_drink,
        methods=['POST']
    )
    app.add_url_rule(
        '/drinks/<int:id>',
        'update_drink',
        update_drink,
        methods=['PATCH']
    )
    app.add_url_rule(
        '/drinks/<int:id>',
        'delete_drink',
        delete_drink,
        methods=['DELETE']
    )
