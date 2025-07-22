from flask import request
from . import sms_bp
from . import services


@sms_bp.route('/test_message', methods=['GET'])
def test_message():
    services.send_confirmation_message()
    return "<h1>Testing sending message!</h1>"

@sms_bp.route('test')
def test():
    return "<h1>SMS Blueprint Route Works!</h1>"