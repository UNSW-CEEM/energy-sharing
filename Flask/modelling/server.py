
from flask import Flask 
from flask import jsonify, request
from flask import make_response
app = Flask(__name__)
import main 
import json

# test
@app.route("/")
def hello():
    print type(request.get_json())
    scenario = {
        'participants':request.get_json()
        }
    result = main.run_en_json(scenario)
    # return json.dumps(result)
    return jsonify(result)

@app.route("/participantNames")
def participantNames():
    result = main.getParticipantNames()
    # return json.dumps(result)
    # result = json.dumps(result)
    # result = {'ids': result}
    return jsonify(result)




@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)