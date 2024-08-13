import azure.functions as func
from azurefunctions.extensions.http.fastapi import Request, JSONResponse
import os
import logging

# from azure.storage.blob import BlobServiceClient, BlobClient

# Azure Function App
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# # Azure Blob Storage
# connection_string = os.environ["OutputBlobConnString"]
# container_name = "output-container"
# blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Maximum chunk size for appending to blob
# MAX_CHUNK_SIZE = 100 * 1024 * 1024  # 100 MB

### FFMPEG ###
import sys
import subprocess

@app.function_name(name="health")
@app.route(route="health", methods=[func.HttpMethod.GET])
def health(req: Request) -> JSONResponse:
    return JSONResponse({"status": "Healthy", "status_code": 200})

@app.function_name(name="testFfmpeg")
@app.route(route="test/ffmpeg", methods=[func.HttpMethod.GET])
def test_ffmpeg(req: Request) -> JSONResponse:
    command = "-h"

    sys.path.append(homebrew_lib_path)
    os.environ['PATH'] = os.path.join(os.getcwd(), 'libs', 'ffmpeg') + ':' + os.environ['PATH']
        
    # context.function_directory returns the current directory in which functions is executed 
    # ffmpeg_path = "/".join([str(context.function_directory), FFMPEG_RELATIVE_PATH])
    ffmpeg_path = "ffmpeg"
    result = subprocess.run([ffmpeg_path, '-version'], capture_output=True, text=True)

    logging.debug(f"ffmpeg_path: {result.stdout}")
    logging.debug(f"Executing command: {ffmpeg_path} {command}")

    try:
        byte_output  = subprocess.check_output([ffmpeg_path, command])
        return JSONResponse({"output": byte_output.decode("utf-8"), "status": "Command executed successfully", "command": command, "status_code": 200}) 
    except Exception as e:
        return JSONResponse({"status": "Error executing command", "error": str(e), "command": command}, status_code=500)

# @app.function_name(name="streamingUpload")
# @app.route(route="stream/upload", methods=[func.HttpMethod.POST])
# # @app.blob_output(arg_name="outputBlob", path="output-container/uploaded_blob.txt", connection="OutputBlobConnString")
# async def streaming_upload(req: Request) -> JSONResponse:
#     """Handle streaming upload requests."""
#     logging.info('Python HTTP trigger function processed a request.')
#     try:
#         blob_name = "uploaded_blob.txt"
#         blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
#         async for chunk in req.stream():
#             response = process_data_chunk(chunk, blob_client)
        
#         return JSONResponse({"status": "Data uploaded and processed successfully"})
#     except Exception as e:
#         logging.error(f"Error processing request: {e}")
#         return JSONResponse({"status": "Error processing data", "error": str(e)}, status_code=500)
# def process_data_chunk(chunk: bytes, blob_client: BlobClient):
#     """Process each data chunk."""
#     chunk_size = len(chunk)
#     if chunk_size == 0:
#         return JSONResponse({"status": "No data received"})
#     # if blob doesn't exist, create
#     if not blob_client.exists():
#         blob_client.create_append_blob()

#     if chunk_size > MAX_CHUNK_SIZE:
#         for i in range(0, chunk_size, MAX_CHUNK_SIZE):
#             end = i + MAX_CHUNK_SIZE
#             blob_client.append_block(chunk[i:end])
#     else:
#         blob_client.append_block(chunk)

#     # return successful response
#     return JSONResponse({"status": "Chunk {} uploaded and processed successfully".format(chunk)})


# # # @app.route(route="streaming_upload", methods=[func.HttpMethod.POST])
# # # async def streaming_upload(req: Request) -> JSONResponse:
# # #     """Handle streaming upload requests."""
# # #     logging.info('Python HTTP trigger function processed a request.')
# # #     try:
# # #         blob_name = "uploaded_blob.txt"
# # #         blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
# # #         # Ensure the blob exists before appending
# # #         if not blob_client.exists():
# # #             blob_client.create_append_blob()
        
# # #         async for chunk in req.stream():
# # #             process_data_chunk(chunk, blob_client)
        
# # #         return JSONResponse({"status": "Data uploaded and processed successfully"})
# # #     except Exception as e:
# # #         logging.error(f"Error processing request: {e}")
# # #         return JSONResponse({"status": "Error processing data", "error": str(e)}, status_code=500)

# # # def process_data_chunk(chunk: bytes, blob_client: BlobClient):
# # #     """Process each data chunk."""
# # #     # logging.info(f"\tData chunk: {chunk}")
# # #     blob_client.append_block(chunk)


# def generate_count():
#     """Generate a stream of chronological numbers."""
#     count = 0
#     while True:
#         yield f"counting, {count}\n\n"
#         count += 1

# @app.route(route="stream", methods=[func.HttpMethod.GET])
# async def stream_count(req: func.HttpRequest) -> StreamingResponse:
#     """Endpoint to stream of chronological numbers."""
#     return StreamingResponse(generate_count(), media_type="text/event-stream")

# @app.route(route="streaming_upload", methods=[func.HttpMethod.POST])
# async def streaming_upload(req: func.HttpRequest) -> JSONResponse:
#     """Handle streaming upload requests."""
#     # Process each chunk of data as it arrives
#     async for chunk in req.stream():
#         process_data_chunk(chunk)

#     # Once all data is received, return a JSON response indicating successful processing
#     return JSONResponse({"status": "Data uploaded and processed successfully"})

# def process_data_chunk(chunk: bytes):
#     """Process each data chunk."""
#     # Add custom processing logic here
#     pass


# @app.route(route="stream_demo_http_trigger")
# def stream_demo_http_trigger(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     name = req.params.get('name')
#     if not name:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             name = req_body.get('name')

#     if name:
#         return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )