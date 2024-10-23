import unittest
import grpc
import pet_pb2
import pet_pb2_grpc

class TestPetAdoptionSystem(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.channel = grpc.insecure_channel('localhost:50051')
        cls.stub = pet_pb2_grpc.PetServiceStub(cls.channel)

    def test_add_pet(self):
        response = self.stub.AddPet(pet_pb2.AddPetRequest(pet=pet_pb2.Pet(
            name="Buddy",
            age=3,
            gender="Male",
            breed="Golden Retriever",
            photo=b'binary_image_data'  # Replace with actual binary image data if needed
        )))
        self.assertEqual(response.pet.name, "Buddy")
        self.assertEqual(response.pet.age, 3)
        self.assertEqual(response.pet.gender, "Male")
        self.assertEqual(response.pet.breed, "Golden Retriever")

    def test_get_pet_by_name(self):
        response = self.stub.GetPet(pet_pb2.GetPetRequest(characteristic="Buddy"))
        self.assertEqual(response.pet.name, "Buddy")

    def test_get_pet_by_breed(self):
        response = self.stub.GetPet(pet_pb2.GetPetRequest(characteristic="Golden Retriever"))
        self.assertEqual(response.pet.breed, "Golden Retriever")

    def test_get_non_existent_pet(self):
        response = self.stub.GetPet(pet_pb2.GetPetRequest(characteristic="Max"))
        self.assertEqual(response.pet.name, "")  # Assuming empty name indicates not found

    def test_add_pet_with_missing_info(self):
        with self.assertRaises(grpc.RpcError) as context:
            response = self.stub.AddPet(pet_pb2.AddPetRequest(pet=pet_pb2.Pet(
                name="",
                age=-1,
                gender="",
                breed="",
                photo=b'binary_image_data'  # Can still include photo data
            )))
        self.assertEqual(context.exception.code(), grpc.StatusCode.INVALID_ARGUMENT)

    @classmethod
    def tearDownClass(cls):
        cls.channel.close()

if __name__ == '__main__':
    unittest.main()
