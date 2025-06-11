import csv
from faker import Faker
import random
from datetime import datetime, timedelta

# Configuração
fake = Faker('pt_BR')  # Português Brasil
NUM_ROWS = 200  # Quantidade de pedidos a gerar
OUTPUT_FILE = 'orders_data.csv'

# Métodos de pagamento e status
PAYMENT_METHODS = ['CREDITO', 'DEBITO', 'PIX', 'BOLETO']
STATUS_OPTIONS = ['PENDENTE', 'PROCESSANDO', 'ENVIADO', 'ENTREGUE', 'CANCELADO']

# Cidades e regiões brasileiras
BRAZILIAN_STATES = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 
    'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 
    'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
]

def generate_orders_data(num_rows, customers_count, products_count):
    data = []
    
    for _ in range(num_rows):
        # Relacionamentos com outras tabelas
        customer_id = random.randint(1, customers_count)
        product_id = random.randint(1, products_count)
        
        # Data do pedido - últimos 6 meses
        order_date = fake.date_between(start_date='-180d', end_date='today')
        
        # Quantidade e preço unitário
        quantity = random.randint(1, 5)
        
        # Simular variação de preço ao longo do tempo (entre 80% e 120% do preço original)
        unit_price = round(random.uniform(0.8, 1.2) * products_prices[product_id], 2)
        
        payment_method = random.choice(PAYMENT_METHODS)
        
        # Dados de entrega
        delivery_city = fake.city()
        delivery_region = random.choice(BRAZILIAN_STATES)
        
        # Tempo de entrega baseado na região (0-3 dias para mesma região, 3-10 para outras)
        if random.random() < 0.3:  # 30% de chance de ser na mesma região (entrega rápida)
            delivery_time_days = random.randint(0, 3)
        else:
            delivery_time_days = random.randint(3, 10)
        
        # Status baseado na data do pedido e tempo de entrega
        days_since_order = (datetime.now().date() - order_date).days
        if days_since_order > delivery_time_days + 5:
            status = 'ENTREGUE'
        elif days_since_order > delivery_time_days:
            status = random.choice(['ENVIADO', 'ENTREGUE'])
        elif days_since_order > 2:
            status = random.choice(['PROCESSANDO', 'ENVIADO'])
        else:
            status = 'PENDENTE'
            
        # 5% de chance de ser cancelado
        if random.random() < 0.05:
            status = 'CANCELADO'
            delivery_time_days = 0  # Cancelados não têm tempo de entrega
        
        data.append({
            'customer_id': customer_id,
            'product_id': product_id,
            'order_date': order_date.strftime('%Y-%m-%d'),
            'quantity': quantity,
            'unit_price': unit_price,
            'payment_method': payment_method,
            'delivery_city': delivery_city,
            'delivery_region': delivery_region,
            'delivery_time_days': delivery_time_days,
            'status': status
        })
    
    return data

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# Primeiro precisamos obter os preços dos produtos para referência
# (Assumindo que você já gerou os produtos anteriormente)
products_prices = {}
try:
    with open('./data/products_data.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for idx, row in enumerate(reader, start=1):
            products_prices[idx] = float(row['selling_price'])
    products_count = len(products_prices)
except FileNotFoundError:
    print("Erro: Arquivo products_data.csv não encontrado.")
    exit()

# Obter quantidade de clientes (assumindo que customers_data.csv existe)
try:
    with open('./data/customers_data.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        customers_count = sum(1 for _ in reader)
except FileNotFoundError:
    print("Erro: Arquivo customers_data.csv não encontrado.")
    exit()

# Gerar e salvar os dados
orders_data = generate_orders_data(NUM_ROWS, customers_count, products_count)
save_to_csv(orders_data, OUTPUT_FILE)

print(f"Dados de pedidos gerados com sucesso e salvos em {OUTPUT_FILE}")
print(f"Total de pedidos gerados: {NUM_ROWS}")
print(f"Clientes referenciados: 1 a {customers_count}")
print(f"Produtos referenciados: 1 a {products_count}")