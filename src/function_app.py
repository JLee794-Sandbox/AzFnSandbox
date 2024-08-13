import azure.functions as func
import azure.durable_functions as df
import logging
import traceback

import subprocess
import sys

def list_installed_packages():
    result = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
    return result.stdout

def get_architecture():
    result = subprocess.run(["uname", "-m"], capture_output=True, text=True)
    return result.stdout.strip()

myApp = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# An HTTP-triggered function with a Durable Functions client binding
@myApp.route(route="orchestrators/{functionName}")
@myApp.durable_client_input(client_name="client")
async def http_start(req: func.HttpRequest, client):
    logging.info("Installed packages:\n{}".format(list_installed_packages()))
    logging.info("System architecture: {}".format(get_architecture()))
    function_name = req.route_params.get('functionName')
    # instance_id = await client.start_new(function_name)
    try:
        import azure
        import azure.storage
        import cffi
        logging.debug("CFFI File: {}".format(cffi.__file__))

        import azure.storage.blob
        return func.HttpResponse(
            "Successfully imported azure.storage.blob",
            status_code=200
        )
    except Exception as e:
        logging.error("Unable to import azure.storage.blob")

        # Log the entire stack to find out what's going on
        traceback.print_stack()
        logging.error(traceback.print_stack())
        logging.error(traceback.format_exc())

        return func.HttpResponse(
            "Unable to import azure.storage.blob",
            status_code=400
        )


    # response = client.create_check_status_response(req, instance_id)
    # return response

# Orchestrator
@myApp.orchestration_trigger(context_name="context")
def hello_orchestrator(context):
    result1 = yield context.call_activity("hello", "Seattle")
    result2 = yield context.call_activity("hello", "Tokyo")
    result3 = yield context.call_activity("hello", "London")

    return [result1, result2, result3]

# Activity
@myApp.activity_trigger(input_name="city")
def hello(city: str):
    return f"Hello {city}"