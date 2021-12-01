from flask import Flask, request, jsonify
from model import *


app = Flask("Test server")


width = 30
height = 30
number_cars = 0
randomModel = None
currentStep = 0


@app.route("/")
def default():
    print("Request Recieved")
    return "Hello there!"


@app.route("/config", methods=['POST'])
def configure():
    global number_cars, width, height, randomModel, currentStep
    number_cars = int(request.form.get("NumberCars"))
    width = int(request.form.get("width"))
    height = int(request.form.get("height"))
    currentStep = 0
    print(
        f"Recieved num_agents = {number_cars}, width = {width}, height = {height}")
    randomModel = RandomModel(number_cars, width, height)

    return jsonify({"OK": number_cars})


@app.route("/updatePosition", methods=['GET'])
def updatePosition():
    global randomModel
    if request.method == 'GET':
        cars_positions = [{"x": x, "y": 0, "z": z} for a, x, z in randomModel.grid.coord_iter(
        ) for agent in a if isinstance(agent, Car)]
        traffic_light_stat = [agent.state for a, x, z in randomModel.grid.coord_iter(
        ) for agent in a if isinstance(agent, Traffic_Light)]
        return jsonify({"cars_positions": cars_positions, "traffic_light_stat": traffic_light_stat})


@app.route("/getCars", methods=['GET'])
def getCars():
    global randomModel
    agentPositions = [{"x": x, "y": 1, "z": z} for (
        b, x, z) in randomModel.grid.coord_iter() for a in b if isinstance(a, Car)]

    return jsonify({'positions': agentPositions})


@app.route('/updateModel', methods=['GET'])
def updateModel():
    global currentStep, randomModel
    randomModel.step()
    currentStep += 1
    return jsonify({'message': f'Model updated to step {currentStep}.', 'currentStep': currentStep})


app.run()
