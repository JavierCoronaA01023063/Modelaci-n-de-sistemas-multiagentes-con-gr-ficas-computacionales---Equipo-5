from flask import Flask, request, jsonify
from model import *


app = Flask("Test server")

numberCars = 0
carModel = None
currentStep = 0


def sortAgents():
    carAgents = []
    for a, x, y in carModel.grid.coord_iter():
        for agent in a:
            if isinstance(agent, Car):
                carAgents.append(agent)

    carAgents.sort(key=lambda x: x.unique_id)

    return carAgents


@app.route("/")
def default():
    print("Request Recieved")
    return "Hello there!"


@app.route("/config", methods=['POST'])
def configure():
    global numberCars, carModel, currentStep
    numberCars = int(request.form.get("numAgents"))
    currentStep = 0
    print(
        f"Recieved num_agents = {numberCars}")
    carModel = RandomModel(numberCars)

    return jsonify({"OK": numberCars})


@app.route("/updatePosition", methods=['GET'])
def updatePosition():
    global carModel
    if request.method == 'GET':
        carAgents = sortAgents()
        cars_positions = [{"x": a.pos[0], "y": 0, "z": a.pos[1]}
                          for (a) in carAgents]
        return jsonify({"positions": cars_positions})


@app.route("/getTrafficLights", methods=['GET'])
def updateTrafficLights():
    global carModel
    traffic_light_stat = [agent.state for a, x, z in carModel.grid.coord_iter(
    ) for agent in a if isinstance(agent, Traffic_Light)]
    return jsonify({"states": traffic_light_stat})


@app.route('/updateModel', methods=['GET'])
def updateModel():
    global currentStep, carModel
    carModel.step()
    currentStep += 1
    return jsonify({'message': f'Model updated to step {currentStep}.', 'currentStep': currentStep})


app.run()
