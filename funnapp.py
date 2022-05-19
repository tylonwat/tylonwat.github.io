"""Runs the web app given a GPT object and UI configuration."""
from http import HTTPStatus
import json
import openai
from flask import Flask, request, Response, render_template
from .gpt import set_openai_key, Example

from dotenv import load_dotenv
import os

load_dotenv()

KEY_NAME = os.getenv('OPENAI_API_KEY')

def fun_app(gpt):
    app = Flask(__name__)
    # if for some reason your conversation with donda gets weird, change the secret key
    app.config['SECRET_KEY'] = '4yoesauj4u'
    set_openai_key(app.config[KEY_NAME])
    set_openai_key(KEY_NAME)


    @app.route("/")
    @app.route("/home")
    def home():
        return render_template("index.html")
       
       
    @app.route("/params", methods=["GET"])
    def get_params():
        output = request.form.to_dict()
        response = output["responce"]
            
        return render_template("index.html", response = response)
     
    def error(err_msg, status_code):
        return Response(json.dumps({"error": err_msg}), status=status_code)

    def get_example(example_id):
        """Gets a single example or all the examples."""
        # return all examples
        if not example_id:
            return json.dumps(gpt.get_all_examples())

        example = gpt.get_example(example_id)
        if not example:
            return error("id not found", HTTPStatus.NOT_FOUND)
        return json.dumps(example.as_dict())

    def post_example():
        """Adds an empty example."""
        new_example = Example("", "")
        gpt.add_example(new_example)
        return json.dumps(gpt.get_all_examples())

    def put_example(args, example_id):
        """Modifies an existing example."""
        if not example_id:
            return error("id required", HTTPStatus.BAD_REQUEST)

        example = gpt.get_example(example_id)
        if not example:
            return error("id not found", HTTPStatus.NOT_FOUND)

        if "input" in args:
            example.input = args["input"]
        if "output" in args:
            example.output = args["output"]

        # update the example
        gpt.add_example(example)
        return json.dumps(example.as_dict())

    def delete_example(example_id):
        """Deletes an example."""
        if not example_id:
            return error("id required", HTTPStatus.BAD_REQUEST)

        gpt.delete_example(example_id)
        return json.dumps(gpt.get_all_examples())

    @app.route(
        "/examples",
        methods=["GET", "POST"],
        defaults={"example_id": ""},
    )
    @app.route(
        "/examples/<example_id>",
        methods=["GET", "PUT", "DELETE"],
    )
    def examples(example_id):
        method = request.method
        args = request.json
        if method == "GET":
            return get_example(example_id)
        if method == "POST":
            return post_example()
        if method == "PUT":
            return put_example(args, example_id)
        if method == "DELETE":
            return delete_example(example_id)
        return error("Not implemented", HTTPStatus.NOT_IMPLEMENTED)

    @app.route("/translate", methods=["GET", "POST"])
    def translate():
        prompt = request.json["prompt"]
        response = gpt.submit_request(prompt)
        offset = 0
        if not gpt.append_output_prefix_to_query:
            offset = len(gpt.output_prefix)
        return {'text': response['choices'][0]['text'][offset:]}
     
     
     
    if __name__ == '__main__': 
         app.run(debug=True)
