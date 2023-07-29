-- Table: datawarehouse.orders

-- DROP TABLE IF EXISTS datawarehouse.orders;

CREATE TABLE IF NOT EXISTS datawarehouse.orders
(
    order_id smallint NOT NULL,
    customer_id bpchar COLLATE pg_catalog."default",
    employee_id smallint,
    order_date date,
    required_date date,
    shipped_date date,
    ship_via smallint,
    freight real,
    ship_name character varying(40) COLLATE pg_catalog."default",
    ship_address character varying(60) COLLATE pg_catalog."default",
    ship_city character varying(15) COLLATE pg_catalog."default",
    ship_region character varying(15) COLLATE pg_catalog."default",
    ship_postal_code character varying(10) COLLATE pg_catalog."default",
    ship_country character varying(15) COLLATE pg_catalog."default",
    PRIMARY KEY (order_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS datawarehouse.orders
    OWNER to northwind_user;

-- Table: datawarehouse.order_details

-- DROP TABLE IF EXISTS datawarehouse.order_details;

CREATE TABLE IF NOT EXISTS datawarehouse.order_details
(
    order_id smallint NOT NULL,
    product_id smallint,
    unit_price real,
    quantity smallint,
    discount real,
    CONSTRAINT order_details_order_id_fkey FOREIGN KEY (order_id)
        REFERENCES datawarehouse.orders (order_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS datawarehouse.order_details
    OWNER to northwind_user;

