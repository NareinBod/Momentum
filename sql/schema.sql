-- Momentum operational data model (MySQL 8+)
CREATE DATABASE IF NOT EXISTS momentum;
USE momentum;

CREATE TABLE suppliers (
  supplier_id INT PRIMARY KEY,
  supplier_name VARCHAR(120) NOT NULL,
  region VARCHAR(60) NOT NULL,
  lead_time_days INT NOT NULL,
  payment_terms_days INT NOT NULL
);

CREATE TABLE products (
  product_id INT PRIMARY KEY,
  sku VARCHAR(30) NOT NULL UNIQUE,
  product_name VARCHAR(140) NOT NULL,
  category VARCHAR(60) NOT NULL,
  unit_cost DECIMAL(12,2) NOT NULL,
  unit_price DECIMAL(12,2) NOT NULL,
  reorder_point INT NOT NULL,
  safety_stock INT NOT NULL
);

CREATE TABLE product_suppliers (
  product_id INT NOT NULL,
  supplier_id INT NOT NULL,
  is_primary BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY (product_id, supplier_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id),
  FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

CREATE TABLE sales_orders (
  order_id BIGINT PRIMARY KEY,
  order_date DATE NOT NULL,
  customer_segment VARCHAR(50) NOT NULL,
  channel VARCHAR(40) NOT NULL
);

CREATE TABLE sales_order_lines (
  order_line_id BIGINT PRIMARY KEY,
  order_id BIGINT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  unit_price DECIMAL(12,2) NOT NULL,
  discount_pct DECIMAL(5,4) NOT NULL DEFAULT 0,
  FOREIGN KEY (order_id) REFERENCES sales_orders(order_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE purchase_orders (
  po_id BIGINT PRIMARY KEY,
  supplier_id INT NOT NULL,
  product_id INT NOT NULL,
  ordered_date DATE NOT NULL,
  promised_date DATE NOT NULL,
  received_date DATE,
  quantity INT NOT NULL,
  unit_cost DECIMAL(12,2) NOT NULL,
  defect_units INT NOT NULL DEFAULT 0,
  FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE INDEX idx_sales_order_date ON sales_orders(order_date);
CREATE INDEX idx_po_supplier_date ON purchase_orders(supplier_id, ordered_date);
