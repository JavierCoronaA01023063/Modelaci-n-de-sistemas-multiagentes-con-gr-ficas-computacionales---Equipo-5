from flask import Flask, request, jsonify
from model import *


app = Flask("Test server")


width = 30
height = 30
num_agents = 0
num_boxes = 0
storageModel = None
currentStep = 0


@app.route("/")
def default():
    print("Request Recieved")
    return "Hello there!"


@app.route("/config", methods=['POST'])
def configure():
    global num_agents, num_boxes, width, height, storageModel, currentStep
    num_agents = int(request.form.get("numAgents"))
    num_boxes = int(request.form.get("numBoxes"))
    width = int(request.form.get("width"))
    height = int(request.form.get("height"))
    currentStep = 0
    print(
        f"Recieved num_agents = {num_agents}, num_boxes = {num_boxes}, width = {width}, height = {height}")
    storageModel = StorageModel(num_agents, num_boxes, width, height)

    return jsonify({"OK": num_agents})


@app.route("/getOrganizing", methods=['GET'])
def getAgents():
    global storageModel
    agentPositions = [{"x": x, "y": 1, "z": z} for (
        b, x, z) in storageModel.grid.coord_iter() for a in b if isinstance(a, OrganizingAgent)]

    return jsonify({'positions': agentPositions})


@app.route("/getBoxes", methods=['GET'])
def getBoxes():
    global storageModel
    agentPositions = [{"x": x, "y": 1, "z": z} for (
        b, x, z) in storageModel.grid.coord_iter() for a in b if isinstance(a, BoxAgent)]

    return jsonify({'positions': agentPositions})


@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, storageModel
    storageModel.step()
    currentStep += 1
    return jsonify({'message': f'Model updated to step {currentStep}.', 'currentStep': currentStep})


app.run()
