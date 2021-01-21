from faker import Faker
import model

fake = Faker()

for i in range(10000):
    profile = fake.profile()
    success, message = model.create_user(
        Username=profile["name"].replace(" ", "_"),
        Password="rootroot",
        FirstName=''.join(profile["name"].split(" ")[:-1]),
        LastName=profile["name"].split(" ")[-1],
        PhoneNumber=fake.phone_number(),
        Email=profile["mail"],
        Faculty=profile['job'],
        Institution=profile['company'],
        Address=profile['address']
    )
    if not success:
        print(message)
