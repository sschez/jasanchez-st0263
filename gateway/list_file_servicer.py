import os
from concurrent import futures
import time
import grpc


import list_files_pb2
import list_files_pb2_grpc


PORT = '50051'

class ListFilesServicer(list_files_pb2_grpc.ListFilesServicer):

    def GetFilesList(self, request, context):
        root_path = os.path.abspath("files")
        print(root_path)

        
        if not os.path.exists(root_path):
            context.set_details('La ruta especificada no existe')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return list_files_pb2.ListFilesResponse()

        files = []
        for item in os.listdir(root_path):
            item_path = os.path.join(root_path, item)
            if os.path.isfile(item_path):
                files.append(list_files_pb2.File(filename=item, file=bytes(item, encoding="utf-8")))

        response = list_files_pb2.ListFilesResponse(files=files)

        return response
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    list_files_pb2_grpc.add_ListFilesServicer_to_server(ListFilesServicer(), server)
    server.add_insecure_port('[::]:' + PORT)
    server.start()
    print('Servidor en ejecución...')
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
