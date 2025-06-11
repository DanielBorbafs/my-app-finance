CREATE DATABASE MARKETPLUS;
GO

USE MARKETPLUS;
GO

CREATE TABLE customers (
    customer_id int primary key IDENTITY(1,1),
    name varchar(40) NOT NULL,
    age int,
    gender char(1) CHECK(gender IN ('F', 'M', 'O')), 
    registration_date date DEFAULT GETDATE(),
    segment varchar(20)
);
GO

CREATE TABLE products(
    product_id int primary key IDENTITY(1,1),
    product_name varchar(30) NOT NULL,
    category varchar(30), 
    cost_price decimal(10,2) CHECK(cost_price >= 0),
    selling_price decimal(10,2) CHECK(selling_price >= 0),
    supplier varchar(20),
    CHECK(selling_price >= cost_price) 
);
GO

CREATE TABLE orders (
    order_id int primary key IDENTITY(1,1), 
    customer_id int NOT NULL,
    product_id int NOT NULL,
    order_date date DEFAULT GETDATE(),
    quantity int CHECK(quantity > 0),
    unit_price decimal(10,2) CHECK(unit_price > 0),
    payment_method varchar(10) NOT NULL
        CHECK (payment_method IN ('CREDITO', 'DEBITO', 'PIX', 'BOLETO')),
    delivery_city varchar(30),
    delivery_region varchar(30),
    delivery_time_days int CHECK(delivery_time_days >= 0),
    status varchar(15) DEFAULT 'PENDENTE'
        CHECK (status IN ('PENDENTE', 'PROCESSANDO', 'ENVIADO', 'ENTREGUE', 'CANCELADO')),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
GO

CREATE TABLE reviews(
    review_id int primary key IDENTITY(1,1),
    order_id int NOT NULL,
    rating int NOT NULL
        CHECK(rating BETWEEN 1 AND 5), -- Corrigido aqui
    review_text text,
    review_date date DEFAULT GETDATE(),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
GO



CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_product ON orders(product_id);
CREATE INDEX idx_reviews_order ON reviews(order_id);
GO