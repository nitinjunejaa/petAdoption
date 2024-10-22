import grpc
import os

import pet_pb2
import pet_pb2_grpc

def add_pet(stub, name, age, gender, breed, photograph_path):
    if not os.path.isfile(photograph_path):
        raise FileNotFoundError(f"No such file: '{photograph_path}'")
    
    with open(photograph_path, 'rb') as f:
        photo_data = f.read()
    
    response = stub.AddPet(pet_pb2.AddPetRequest(pet=pet_pb2.Pet(
        name=name,
        age=age,
        gender=gender,
        breed=breed,
        photo=photo_data
    )))
    print("Added Pet:", response.pet)

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = pet_pb2_grpc.PetServiceStub(channel)
        add_pet(stub, "Buddy", 3, "Male", "Golden Retriever", "/home/freyajindal22/Documents/petAdoption/buddy.jpg") 

if __name__ == '__main__':
    run()
