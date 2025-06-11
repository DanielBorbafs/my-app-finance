import csv
from faker import Faker
import random
from datetime import datetime, timedelta

# Configuração
fake = Faker('pt_BR')  # Português Brasil
NUM_REVIEWS = 150  # Quantidade de avaliações a gerar
OUTPUT_FILE = 'reviews_data.csv'

# Textos de avaliação pré-definidos (positivos, neutros e negativos)
POSITIVE_REVIEWS = [
    "Produto excelente, superou minhas expectativas!",
    "Muito bom, recomendo a todos!",
    "Qualidade impressionante, vale cada centavo.",
    "Entrega rápida e produto perfeito.",
    "Adorei, exatamente como na descrição."
]

NEUTRAL_REVIEWS = [
    "Produto ok, mas poderia ser melhor.",
    "Não é ruim, mas também não é excelente.",
    "Cumpre o básico, nada especial.",
    "Esperava um pouco mais pelo preço.",
    "Funciona, mas a qualidade é mediana."
]

NEGATIVE_REVIEWS = [
    "Produto veio com defeito, muito decepcionado.",
    "Qualidade péssima, não compraria novamente.",
    "Demorou muito para chegar e veio errado.",
    "Não funciona como descrito, quero meu dinheiro de volta.",
    "Pior compra que já fiz, não recomendo."
]

def generate_review_text(rating):
    """Gera texto de avaliação baseado na nota"""
    if rating >= 4:
        return random.choice(POSITIVE_REVIEWS)
    elif rating == 3:
        return random.choice(NEUTRAL_REVIEWS)
    else:
        return random.choice(NEGATIVE_REVIEWS)

def generate_reviews_data(num_reviews, orders_count):
    data = []
    
    # Garantir que não vamos gerar mais reviews que pedidos existentes
    num_reviews = min(num_reviews, orders_count)
    
    # Criar lista de order_ids disponíveis e embaralhar
    order_ids = list(range(1, orders_count + 1))
    random.shuffle(order_ids)
    
    for i in range(num_reviews):
        order_id = order_ids[i]
        
        # Gerar rating com distribuição mais positiva (mais 4 e 5 estrelas)
        rating = random.choices(
            [1, 2, 3, 4, 5],
            weights=[5, 10, 15, 30, 40]  # Probabilidades relativas
        )[0]
        
        # 20% de chance de não ter texto de avaliação
        review_text = generate_review_text(rating) if random.random() > 0.2 else None
        
        # Data da avaliação - até 15 dias após a data do pedido
        review_date = fake.date_between(start_date='-60d', end_date='today')
        
        data.append({
            'order_id': order_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date.strftime('%Y-%m-%d')
        })
    
    return data

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# Obter quantidade de pedidos (assumindo que orders_data.csv existe)
try:
    with open('./data/orders_data.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        orders_count = sum(1 for _ in reader)
except FileNotFoundError:
    print("Erro: Arquivo orders_data.csv não encontrado.")
    exit()

# Gerar e salvar os dados
reviews_data = generate_reviews_data(NUM_REVIEWS, orders_count)
save_to_csv(reviews_data, OUTPUT_FILE)

print(f"Dados de avaliações gerados com sucesso e salvos em {OUTPUT_FILE}")
print(f"Total de avaliações geradas: {len(reviews_data)}")
print(f"Pedidos avaliados: {len(reviews_data)} de {orders_count} disponíveis")