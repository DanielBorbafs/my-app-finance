import csv
from faker import Faker
import random

# Configuração
fake = Faker('pt_BR')  # Português Brasil
NUM_ROWS = 50  # Quantidade de produtos a gerar
OUTPUT_FILE = './data/products_data.csv'

# Categorias e fornecedores fictícios
CATEGORIES = [
    'Consoles', 'Acessórios Gamer', 'PC Gamer', 'Periféricos', 'Jogos',
    'Hardware', 'Streaming', 'Realidade Virtual', 'Monitores', 'Cadeiras Gamer'
]


SUPPLIERS = [
    'TechPro Distribuidora', 'GamerX Brasil', 'LevelUp Supply', 'DigitalZone',
    'XPTech Importados', 'GameWorld Ltda', 'UltraGamer Distribuição', None
]

def generate_product_name(category):
    """Gera nomes de produtos baseados na categoria"""
    base_names = {
        'Consoles': ['PlayStation 5', 'Xbox Series X', 'Nintendo Switch OLED', 'Steam Deck', 'PlayStation 4 Pro'],
        'Acessórios Gamer': ['Controle PS5', 'Volante Logitech', 'Headset Gamer RGB', 'Base de Carregamento', 'Suporte para Console'],
        'PC Gamer': ['Desktop Ryzen 7 RTX 4060', 'PC Intel i7 RTX 4070', 'Mini PC Gamer RGB', 'Setup Gamer Completo', 'Workstation Gamer'],
        'Periféricos': ['Teclado Mecânico RGB', 'Mouse Gamer 16000 DPI', 'Mousepad Extra Grande', 'Headset Surround 7.1', 'Hub USB RGB'],
        'Jogos': ['God of War Ragnarok', 'Elden Ring', 'FIFA 25', 'Call of Duty MW3', 'Zelda: Tears of the Kingdom'],
        'Hardware': ['Placa de Vídeo RTX 4080', 'SSD NVMe 1TB', 'Fonte 750W 80 Plus', 'Placa-mãe B550', 'Water Cooler ARGB'],
        'Streaming': ['Webcam 4K Logitech', 'Microfone Condensador USB', 'Placa de Captura Elgato', 'Ring Light RGB', 'Stream Deck'],
        'Realidade Virtual': ['Meta Quest 3', 'PlayStation VR2', 'HTC Vive Pro 2', 'Acessório VR Tracker', 'Head Strap Reforçado'],
        'Monitores': ['Monitor 27" 240Hz', 'Monitor Curvo Ultrawide', 'Monitor 4K Gamer', 'Monitor IPS 165Hz', 'Monitor Portátil'],
        'Cadeiras Gamer': ['Cadeira Reclinável RGB', 'Cadeira Gamer com Apoio de Pé', 'Cadeira Ergonômica Pro', 'Cadeira com Almofadas Memory Foam', 'Cadeira Estilo Racing']
    }
    
    if category in base_names:
        base = random.choice(base_names[category])
        return f"{base} {fake.word().capitalize()}"
    return fake.catch_phrase()

def generate_products_data(num_rows):
    data = []
    for _ in range(num_rows):
        category = random.choice(CATEGORIES)
        product_name = generate_product_name(category)
        
        # Preço de custo entre 10 e 1000 com margem de lucro de 20% a 200%
        cost_price = round(random.uniform(10, 1000), 2)
        margin = random.uniform(0.2, 2.0)  # Margem de 20% a 200%
        selling_price = round(cost_price * (1 + margin), 2)
        
        # Garantindo que selling_price >= cost_price (mesmo que a margem seja negativa por algum erro)
        selling_price = max(selling_price, cost_price)
        
        # 15% de chance de supplier ser NULL
        supplier = random.choice(SUPPLIERS) if random.random() > 0.05 else None
        
        data.append({
            'product_name': product_name[:30],  # Garantindo que não ultrapasse 30 caracteres
            'category': category,
            'cost_price': cost_price,
            'selling_price': selling_price,
            'supplier': supplier
        })
    
    return data

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# Gerar e salvar os dados
products_data = generate_products_data(NUM_ROWS)
save_to_csv(products_data, OUTPUT_FILE)

print(f"Dados de produtos gerados com sucesso e salvos em {OUTPUT_FILE}")
print(f"Total de produtos gerados: {NUM_ROWS}")