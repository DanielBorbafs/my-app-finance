import csv
from faker import Faker
from datetime import datetime, timedelta
import random


"""Table customers {
  customer_id integer pk
  name varchar(40)
  age int
  gender CHAR(1)
  registration_date date
  segment varchar(20)
}"""
# Configuração
fake = Faker('pt_BR')  # Português Brasil
NUM_ROWS = 1000
OUTPUT_FILE = './data/customers_data.csv'

# Opções para os campos
GENDERS = ['F', 'M', 'O']
SEGMENTS = ['Vip', 'Medium', 'Basic', None]

def generate_customers_data(num_rows):
    data = []
    for _ in range(num_rows):
        name = fake.name()
        age = random.randint(18, 75)
        gender = random.choice(GENDERS)
    
        registration_date = fake.date_between(start_date='-1y', end_date='today')
        
       
        segment = random.choice(SEGMENTS) if random.random() > 0.1 else None
        
        data.append({
            'name': name,
            'age': age,
            'gender': gender,
            'registration_date': registration_date.strftime('%Y-%m-%d'),
            'segment': segment
        })
    
    return data

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# Gerar e salvar os dados
customers_data = generate_customers_data(NUM_ROWS)
save_to_csv(customers_data, OUTPUT_FILE)

print(f"Dados gerados com sucesso e salvos em {OUTPUT_FILE}")