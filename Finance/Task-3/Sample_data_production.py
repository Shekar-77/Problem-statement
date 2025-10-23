import pandas as pd
import random
import faker

fake = faker.Faker()

def generate_synthetic_aadhaar():
    return ''.join([str(random.randint(0, 9)) for _ in range(12)])

data = []
for _ in range(1000):  # generate 1000 fake entries
    data.append({
        "Aadhaar": generate_synthetic_aadhaar(),
        "Name": fake.name(),
        "DOB": fake.date_of_birth(minimum_age=18, maximum_age=80),
        "Address": fake.address(),
        "Phone": fake.phone_number(),
        "Email": fake.email()
    })

df = pd.DataFrame(data)
df.to_csv("synthetic_aadhaar_data.csv", index=False)
print(df.head())
