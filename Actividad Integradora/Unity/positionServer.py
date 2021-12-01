from flask import Flask, request, jsonify
from model import *


app = Flask("Test server")


width = 30
height = 30
num_agents = 0
num_boxes = 0
storageModel = None
currentStep = 0


def sortAgents():
    organizingAgents = []
    boxAgents = []
    for a, x, y in storageModel.grid.coord_iter():
        for agent in a:
            if isinstance(agent, OrganizingAgent):
                organizingAgents.append(agent)
            elif isinstance(agent, BoxAgent):
                boxAgents.append(agent)

    organizingAgents.sort(key=lambda x: x.unique_id)
    boxAgents.sort(key=lambda x: x.unique_id)

    return organizingAgents, boxAgents


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
    organizingAgents, boxAgents = sortAgents()
    agentPositions = [{"x": a.pos[0], "y": 0.5, "z": a.pos[1]}
                      for (a) in organizingAgents]

    return jsonify({'positions': agentPositions})


@app.route("/getBoxes", methods=['GET'])
def getBoxes():
    global storageModel
    organizingAgents, boxAgents = sortAgents()
    agentPositions = [{"x": a.pos[0], "y": 0.5, "z": a.pos[1]}
                      for (a) in boxAgents]

    return jsonify({'positions': agentPositions})


@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, storageModel
    storageModel.step()
    currentStep += 1
    return jsonify({'message': f'Model updated to step {currentStep}.', 'currentStep': currentStep})


app.run()
