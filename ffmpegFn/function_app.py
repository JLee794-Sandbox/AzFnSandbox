import azure.functions as func
import logging
# import os 

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

import subprocess

FFMPEG_RELATIVE_PATH = "dependencies/ffmpeg"
# FILE_SHARE_MOUNT_PATH = os.environ['FILE_SHARE_MOUNT_PATH']

@app.route(route="ffmpeg_test")
def http_trigger(req: func.HttpRequest,
                    context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    command = req.params.get('command')
    # If no command specified, set the command to help
    if not command:
        command = "-h"

    # context.function_directory returns the current directory in which functions is executed 
    ffmpeg_path = "/".join([str(context.function_directory), FFMPEG_RELATIVE_PATH])

    try:
        byte_output  = subprocess.check_output([ffmpeg_path, command])
        return func.HttpResponse(byte_output.decode('UTF-8').rstrip(),status_code=200)
    except Exception as e:
        return func.HttpResponse("Unexpected exception happened when executing ffmpeg. Error message:" + str(e),status_code=200)