
-------------------------------------- Análises introdutórias das vendas
-- Venda total em R$
SELECT 
	SUM(QUANTITY * UNIT_PRICE) AS VENDA_TOTAL
FROM 
	ORDERS 
WHERE
	STATUS = 'ENTREGUE'
GO

-- QUANTIDADE DE PEDIDOS CANCELADOS
SELECT COUNT(ORDER_ID) AS PEDIDOS_CANCELADOS
FROM orders
WHERE STATUS = 'CANCELADO'
GO

-- QUANTIDADE DE PEDIDOS EM PROCESSO
SELECT COUNT(ORDER_ID) AS PEDIDOS_PROCESSANDO
FROM orders
WHERE STATUS = 'PROCESSANDO'
GO

-- PRINCIPAIS METODOS DE PAGAMENTO
SELECT PAYMENT_METHOD, COUNT(CUSTOMER_ID) AS QUANTIDADE
FROM ORDERS 
GROUP BY payment_method
ORDER BY QUANTIDADE DESC
GO

-- DISTRIBUIÇÃO DEMOGRÁFICA DOS CLIENTES, QUANTIDADE POR ESTADO
SELECT delivery_region, COUNT(customer_id) AS DISTRIBUIÇÃO
FROM ORDERS
GROUP BY delivery_region
ORDER BY DISTRIBUIÇÃO DESC
GO


----------------------------------------- -Análises introdutórias dos clientes

-- QUANTIDADE TOTAL DE CLIENTES
SELECT COUNT(customer_id) as Qtd_clientes
FROM customers 
GO

-- CONTAGEM DE CLIENTES AGRUPADOS POR GÊNERO
SELECT gender, COUNT(customer_id) AS Distribuições
FROM customers 
GROUP BY gender
GO

-- CORRIGINDO CAMPOS VAZIOS(SEGMENT)
/*
 * Regras de negócios
 VIP = Clientes que compram mais de 1m
 MEDIUM = Clientes que compram entre 150000 E 999999
*/

UPDATE c
SET c.segment = 'Vip'
FROM customers c
WHERE segment = ''
	AND EXISTS(
		SELECT 1 
		FROM orders o 
		WHERE o.customer_id = c.customer_id
			AND o.unit_price >= 100000.00
);


UPDATE c
SET c.segment = 'MEDIUM'
FROM customers c
WHERE segment = ''
	AND EXISTS(
		SELECT 1 
		FROM orders o 
		WHERE o.customer_id = c.customer_id
			AND o.unit_price BETWEEN 1 AND 100000
);


-- SEGMENTANDO OS CLIENTES POR r$
UPDATE c
SET c.segment = 'Vip'
FROM customers c
INNER JOIN orders o ON o.customer_id = c.customer_id
WHERE c.segment = 'Basic' AND o.unit_price >= 100000.00
GO

UPDATE c
SET c.segment = 'Medium'
FROM customers c
INNER JOIN orders o ON o.customer_id = c.customer_id
WHERE c.segment = 'Vip'
  AND o.unit_price BETWEEN 10000.00 AND 99999.00
GO

