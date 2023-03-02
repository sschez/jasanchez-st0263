import grpc
import list_files_pb2
import list_files_pb2_grpc


def list_files():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = list_files_pb2_grpc.ListFilesStub(channel)
        response = stub.GetFilesList(list_files_pb2.ListFilesRequest())
        for file in response.files:
            print(file.filename)

if __name__ == '__main__':
    list_files()
