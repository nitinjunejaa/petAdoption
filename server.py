import grpc
from concurrent import futures
import time

import pet_pb2
import pet_pb2_grpc

# In-memory storage for pets
pets = {}

class PetService(pet_pb2_grpc.PetServiceServicer):
    def AddPet(self, request, context):
        pet_data = request.pet
        pets[pet_data.name] = pet_data
        return pet_pb2.PetResponse(pet=pet_data)

    def GetPet(self, request, context):
        characteristic = request.characteristic
        # Search by name or breed
        for pet in pets.values():
            if (pet.name == characteristic) or (pet.breed == characteristic):
                return pet_pb2.PetResponse(pet=pet)
        return pet_pb2.PetResponse()  # Return empty if not found

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # Multithreading support
    pet_pb2_grpc.add_PetServiceServicer_to_server(PetService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server is running on port 50051...")
    
    try:
        while True:
            time.sleep(86400)  # Keep the server alive for a day
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
