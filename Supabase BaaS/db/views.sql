-- Vistas hechas:



-- ================== Sales fact ==================
CREATE OR REPLACE VIEW public.v_sales_fact
AS
SELECT 
    i.id as invoice_id,
    i.invoice_date,
    i.customer_id,
    c.name as customer_name,
    i.total_amount as invoice_total,
    COUNT(il.id) as total_items,
    SUM(il.quantity) as total_quantity,
    i.created_at
FROM public.invoices i
INNER JOIN public.customers c ON i.customer_id = c.id
INNER JOIN public.invoice_lines il ON i.id = il.invoice_id
GROUP BY 
    i.id,
    i.invoice_date, 
    i.customer_id, 
    c.name, 
    i.total_amount, 
    i.created_at;



-- ================== Sales by fact ==================
CREATE OR REPLACE VIEW public.v_sales_by_category
AS
SELECT 
    cat.id as category_id,
    cat.name as category_name,
    COUNT(DISTINCT i.id) as total_invoices,
    SUM(il.quantity) as total_quantity_sold,
    SUM(il.line_total) as total_sales_amount
FROM public.categories cat
INNER JOIN public.products p ON cat.id = p.category_id
INNER JOIN public.invoice_lines il ON p.id = il.product_id
INNER JOIN public.invoices i ON il.invoice_id = i.id
GROUP BY cat.id, cat.name;



-- ================== Sales by country ==================
CREATE OR REPLACE VIEW public.v_sales_by_country
AS
SELECT 
    co.code as country_code,
    co.name as country_name,
    COUNT(DISTINCT i.id) as total_invoices,
    COUNT(DISTINCT c.id) as total_customers,
    SUM(il.quantity) as total_quantity_sold,
    SUM(il.line_total) as total_sales_amount,
    AVG(il.line_total) as avg_sale_amount
FROM public.countries co
INNER JOIN public.customers c ON co.code = c.country_code
INNER JOIN public.invoices i ON c.id = i.customer_id
INNER JOIN public.invoice_lines il ON i.id = il.invoice_id
GROUP BY co.code, co.name
ORDER BY total_sales_amount DESC;



-- ================== Sales top 30d ==================
CREATE OR REPLACE VIEW public.v_top_products_30d
AS
SELECT 
    p.id as product_id,
    p.name as product_name,
    c.name as category_name,
    SUM(il.quantity) as total_quantity_sold,
    SUM(il.line_total) as total_sales_amount,
    COUNT(DISTINCT i.id) as total_invoices,
    AVG(il.unit_price) as avg_unit_price,
    RANK() OVER (ORDER BY SUM(il.line_total) DESC) as sales_rank
FROM public.products p
INNER JOIN public.categories c ON p.category_id = c.id
INNER JOIN public.invoice_lines il ON p.id = il.product_id
INNER JOIN public.invoices i ON il.invoice_id = i.id
WHERE i.invoice_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY p.id, p.name, c.name
ORDER BY total_sales_amount DESC;

