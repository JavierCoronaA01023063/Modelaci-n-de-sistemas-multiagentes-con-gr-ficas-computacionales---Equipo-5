from flask import Flask, request, jsonify

app = Flask("Test server")


width = 30
height = 30
num_agents = 0
num_boxes = 0


@app.route("/")
def default():
    print("Request Recieved")
    return "Hello there!"


@app.route("/config", methods=['POST'])
def configure():
    global num_agents
    global num_boxes
    global width
    global height
    num_agents = int(request.form.get("numAgents"))
    num_boxes = int(request.form.get("numBoxes"))
    width = int(request.form.get("width"))
    height = int(request.form.get("height"))
    print(
        f"Recieved num_agents = {num_agents}, num_boxes = {num_boxes}, width = {width}, height = {height}")
    return jsonify({"OK": num_agents})


@app.route("/update", methods=['GET'])
def update_points():
    pass


app.run()
