--====================================DDL====================================
-- Dominios
create table if not exists public.countries (
    code text primary key,
    name text not null
);

create table if not exists public.categories (
    id bigint generated always as identity primary key,
    name text not null unique
);
-- Comercial
create table if not exists public.products (
    id bigint generated always as identity primary key,
    name text not null,
    category_id bigint not null references public.categories(id),
    unit_price numeric(12,2) not null check (unit_price >= 0),
    created_at timestamptz default now()
);

create table if not exists public.customers (
    id bigint generated always as identity primary key,
    name text not null,
    email text,
    country_code text not null references public.countries(code),
    created_at timestamptz default now()
);

create table if not exists public.invoices (
    id bigint generated always as identity primary key,
    customer_id bigint not null references public.customers(id),
    invoice_date date not null default current_date,
    total_amount numeric(14,2) not null default 0,
    created_at timestamptz default now()
);

create table if not exists public.invoice_lines (
    id bigint generated always as identity primary key,
    invoice_id bigint not null references public.invoices(id) on delete cascade,
    product_id bigint not null references public.products(id),
    quantity numeric(12,2) not null check (quantity > 0),
    unit_price numeric(12,2) not null check (unit_price >= 0),
    line_total numeric(14,2) not null check (line_total >= 0)
);
-- Tablas de Autorización (para RLS)
create table if not exists public.user_allowed_country (
    user_id uuid not null,
    country_code text not null references public.countries(code),
    primary key (user_id, country_code)
);

create table if not exists public.user_allowed_category (
    user_id uuid not null,
    category_id bigint not null references public.categories(id),
    primary key (user_id, category_id)
);
--====================================RLS====================================
alter table public.countries disable row level security;
alter table public.categories disable row level security;
alter table public.products enable row level security;
alter table public.customers enable row level security;
alter table public.invoices enable row level security;
alter table public.invoice_lines enable row level security;
alter table public.user_allowed_country disable row level security;
alter table public.user_allowed_category disable row level security;

--Politicas por categoria (products)

create policy "products_by_user_category_select"
on public.products for select
to authenticated
using (exists (
 select 1 from public.user_allowed_category u
 where u.user_id = auth.uid() and u.category_id = products.category_id
));

create policy "products_by_user_category_insert"
on public.products for insert
to authenticated
with check (exists (
 select 1 from public.user_allowed_category u
 where u.user_id = auth.uid() and u.category_id = products.category_id
));

create policy "products_by_user_category_update"
on public.products for update
to authenticated
using (exists (
 select 1 from public.user_allowed_category u
 where u.user_id = auth.uid() and u.category_id = products.category_id
))
with check (exists (
 select 1 from public.user_allowed_category u
 where u.user_id = auth.uid() and u.category_id = products.category_id
));

create policy "products_by_user_category_delete"
on public.products for delete
to authenticated
using (exists (
 select 1 from public.user_allowed_category u
 where u.user_id = auth.uid() and u.category_id = products.category_id
));

--Politicas por pais (Customers)

create policy "customers_by_user_country_select"
on public.customers for select
to authenticated
using (exists (
 select 1 from public.user_allowed_country u
 where u.user_id = auth.uid() and u.country_code =
customers.country_code
));

create policy "customers_by_user_country_insert"
on public.customers for insert
to authenticated
with check (exists (
 select 1 from public.user_allowed_country u
 where u.user_id = auth.uid() and u.country_code =
customers.country_code
));

create policy "customers_by_user_country_update"
on public.customers for update
to authenticated
using (exists (
 select 1 from public.user_allowed_country u
 where u.user_id = auth.uid() and u.country_code =
customers.country_code
))
with check (exists (
 select 1 from public.user_allowed_country u
 where u.user_id = auth.uid() and u.country_code =
customers.country_code
));

create policy "customers_by_user_country_delete"
on public.customers for delete
to authenticated
using (exists (
 select 1 from public.user_allowed_country u
 where u.user_id = auth.uid() and u.country_code =
customers.country_code
));

--Políticas en invoices (por país del cliente)

create policy "invoices_by_user_country_select"
on public.invoices for select
to authenticated
using (exists (
 select 1
 from public.customers c
 join public.user_allowed_country u
 on u.country_code = c.country_code and u.user_id = auth.uid()
 where c.id = invoices.customer_id
));

create policy "invoices_by_user_country_insert"
on public.invoices for insert
to authenticated
with check (exists (
 select 1
 from public.customers c
 join public.user_allowed_country u
 on u.country_code = c.country_code and u.user_id = auth.uid()
 where c.id = invoices.customer_id
));

create policy "invoices_by_user_country_update"
on public.invoices for update
to authenticated
using (exists (
 select 1
 from public.customers c
 join public.user_allowed_country u
 on u.country_code = c.country_code and u.user_id = auth.uid()
 where c.id = invoices.customer_id
))
with check (exists (
 select 1
 from public.customers c
 join public.user_allowed_country u
 on u.country_code = c.country_code and u.user_id = auth.uid()
 where c.id = invoices.customer_id
));

create policy "invoices_by_user_country_delete"
on public.invoices for delete
to authenticated
using (exists (
 select 1
 from public.customers c
 join public.user_allowed_country u
 on u.country_code = c.country_code and u.user_id = auth.uid()
 where c.id = invoices.customer_id
));

--Políticas en invoice_lines (por país y categoría)

create policy "lines_by_country_and_category_select"
on public.invoice_lines for select
to authenticated
using (
 exists (
 select 1
 from public.invoices i
 join public.customers c on c.id = i.customer_id
 join public.user_allowed_country uc
 on uc.country_code = c.country_code and uc.user_id = auth.uid()
 where i.id = invoice_lines.invoice_id
 )
 and
 exists (
 select 1
 from public.products p
 join public.user_allowed_category ug
 on ug.category_id = p.category_id and ug.user_id = auth.uid()
 where p.id = invoice_lines.product_id
 )
);

create policy "lines_by_country_and_category_cud"
on public.invoice_lines for all
to authenticated
using (
 exists (
 select 1
 from public.invoices i
 join public.customers c on c.id = i.customer_id
 join public.user_allowed_country uc
 on uc.country_code = c.country_code and uc.user_id = auth.uid()
 where i.id = invoice_lines.invoice_id
 )
 and
 exists (
 select 1
 from public.products p
 join public.user_allowed_category ug
 on ug.category_id = p.category_id and ug.user_id = auth.uid()
 where p.id = invoice_lines.product_id
 )
)
with check (
 exists (
 select 1
 from public.invoices i
 join public.customers c on c.id = i.customer_id
 join public.user_allowed_country uc
 on uc.country_code = c.country_code and uc.user_id = auth.uid()
 where i.id = invoice_lines.invoice_id
 )
 and
 exists (
 select 1
 from public.products p
 join public.user_allowed_category ug
 on ug.category_id = p.category_id and ug.user_id = auth.uid()
 where p.id = invoice_lines.product_id
 )
);

-- COUNTRIES (búsquedas por código)
CREATE INDEX IF NOT EXISTS idx_countries_code ON public.countries(code);

-- CATEGORIES (búsquedas por nombre)
CREATE INDEX IF NOT EXISTS idx_categories_name ON public.categories(name);

-- PRODUCTS (RLS y búsquedas frecuentes)
CREATE INDEX IF NOT EXISTS idx_products_category_id ON public.products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_name ON public.products(name);
CREATE INDEX IF NOT EXISTS idx_products_created_at ON public.products(created_at);
CREATE INDEX IF NOT EXISTS idx_products_price ON public.products(unit_price);

-- CUSTOMERS (RLS y búsquedas)
CREATE INDEX IF NOT EXISTS idx_customers_country_code ON public.customers(country_code);
CREATE INDEX IF NOT EXISTS idx_customers_email ON public.customers(email);
CREATE INDEX IF NOT EXISTS idx_customers_name ON public.customers(name);
CREATE INDEX IF NOT EXISTS idx_customers_created_at ON public.customers(created_at);

-- INVOICES (consultas por fecha y cliente)
CREATE INDEX IF NOT EXISTS idx_invoices_customer_id ON public.invoices(customer_id);
CREATE INDEX IF NOT EXISTS idx_invoices_invoice_date ON public.invoices(invoice_date);
CREATE INDEX IF NOT EXISTS idx_invoices_created_at ON public.invoices(created_at);
CREATE INDEX IF NOT EXISTS idx_invoices_total_amount ON public.invoices(total_amount);

-- INVOICE_LINES (joins frecuentes)
CREATE INDEX IF NOT EXISTS idx_invoice_lines_invoice_id ON public.invoice_lines(invoice_id);
CREATE INDEX IF NOT EXISTS idx_invoice_lines_product_id ON public.invoice_lines(product_id);
CREATE INDEX IF NOT EXISTS idx_invoice_lines_unit_price ON public.invoice_lines(unit_price);
CREATE INDEX IF NOT EXISTS idx_invoice_lines_quantity ON public.invoice_lines(quantity);

-- RLS (optimización de joins)
CREATE INDEX IF NOT EXISTS idx_user_allowed_country_user_id ON public.user_allowed_country(user_id);
CREATE INDEX IF NOT EXISTS idx_user_allowed_country_country_code ON public.user_allowed_country(country_code);
CREATE INDEX IF NOT EXISTS idx_user_allowed_country_composite ON public.user_allowed_country(user_id, country_code);

CREATE INDEX IF NOT EXISTS idx_user_allowed_category_user_id ON public.user_allowed_category(user_id);
CREATE INDEX IF NOT EXISTS idx_user_allowed_category_category_id ON public.user_allowed_category(category_id);
CREATE INDEX IF NOT EXISTS idx_user_allowed_category_composite ON public.user_allowed_category(user_id, category_id);

-- Índices compuestos para consultas avanzadas ------------!!!!!!!!!!!!!!!!!!!!!!
CREATE INDEX IF NOT EXISTS idx_products_category_price ON public.products(category_id, unit_price);
CREATE INDEX IF NOT EXISTS idx_invoices_customer_date ON public.invoices(customer_id, invoice_date);
CREATE INDEX IF NOT EXISTS idx_invoice_lines_invoice_product ON public.invoice_lines(invoice_id, product_id);


-- =======POBLADO=======

insert into public.countries (code, name) values
('CR', 'Costa Rica'),
('US', 'United States'),
('CA', 'Canada'),
('GB', 'United Kingdom'),
('DE', 'Germany'),
('FR', 'France'),
('ES', 'Spain'),
('IT', 'Italy'),
('JP', 'Japan'),
('AU', 'Australia'),
('BR', 'Brazil'),
('MX', 'Mexico'),
('AR', 'Argentina'),
('CL', 'Chile'),
('CO', 'Colombia'),
('PE', 'Peru'),
('NL', 'Netherlands'),
('SE', 'Sweden'),
('NO', 'Norway'),
('CH', 'Switzerland');

-- Categories (20 categorías)
insert into public.categories (name) values
('Electronics'),
('Furniture'),
('Beauty'),
('Food'),
('Clothing'),
('Sports'),
('Books'),
('Home & Garden'),
('Automotive'),
('Toys'),
('Health'),
('Music'),
('Office Supplies'),
('Pet Supplies'),
('Jewelry'),
('Tools'),
('Art & Crafts'),
('Baby Products'),
('Travel'),
('Gaming');

-- Products (20 productos distribuidos en diferentes categorías)
insert into public.products (name, category_id, unit_price) values
('Smartphone Model X', (select id from public.categories where name = 'Electronics'), 699.00),
('Laptop Pro 15"', (select id from public.categories where name = 'Electronics'), 1299.00),
('Wireless Headphones', (select id from public.categories where name = 'Electronics'), 199.99),
('4K Smart TV 55"', (select id from public.categories where name = 'Electronics'), 849.99),
('Gaming Console Pro', (select id from public.categories where name = 'Gaming'), 499.99),

('Wooden Dining Table', (select id from public.categories where name = 'Furniture'), 499.00),
('Office Chair Ergo', (select id from public.categories where name = 'Furniture'), 149.50),
('Modern Sofa 3-Seater', (select id from public.categories where name = 'Furniture'), 799.00),
('Standing Desk Adjustable', (select id from public.categories where name = 'Furniture'), 329.99),

('Hydrating Face Cream', (select id from public.categories where name = 'Beauty'), 29.99),
('Anti-Aging Serum', (select id from public.categories where name = 'Beauty'), 45.00),
('Professional Hair Dryer', (select id from public.categories where name = 'Beauty'), 89.99),

('Organic Olive Oil 1L', (select id from public.categories where name = 'Food'), 12.75),
('Premium Coffee Beans 500g', (select id from public.categories where name = 'Food'), 24.99),
('Artisan Honey 250ml', (select id from public.categories where name = 'Food'), 18.50),

('T-Shirt Classic', (select id from public.categories where name = 'Clothing'), 19.90),
('Denim Jeans Premium', (select id from public.categories where name = 'Clothing'), 79.99),
('Winter Jacket Waterproof', (select id from public.categories where name = 'Clothing'), 149.99),

('Running Shoes Professional', (select id from public.categories where name = 'Sports'), 129.00),
('Yoga Mat Premium', (select id from public.categories where name = 'Sports'), 39.99);

-- Customers (20 clientes distribuidos en diferentes países)
insert into public.customers (name, email, country_code) values
('Natalia Orozco', 'natalia.orozco@ejemplo.cr', 'CR'),
('Isaac Villalobos', 'isaac.villalobos@ejemplo.us', 'CR'),
('Carlos Abarca', 'carlos.abarca@ejemplo.fr', 'CR'),
('Dilan Hernandez', 'dilan.hernandez@ejemplo.de', 'CR'),
('Maria Rodriguez', 'maria.rodriguez@ejemplo.es', 'ES'),
('John Smith', 'john.smith@ejemplo.ca', 'CA'),
('Sophie Martin', 'sophie.martin@ejemplo.fr', 'US'),
('Hans Mueller', 'hans.mueller@ejemplo.de', 'DE'),
('Emma Wilson', 'emma.wilson@ejemplo.gb', 'GB'),
('Luca Rossi', 'luca.rossi@ejemplo.it', 'IT'),
('Yuki Tanaka', 'yuki.tanaka@ejemplo.jp', 'JP'),
('Sarah Johnson', 'sarah.johnson@ejemplo.au', 'AU'),
('Pedro Silva', 'pedro.silva@ejemplo.br', 'BR'),
('Ana Garcia', 'ana.garcia@ejemplo.mx', 'MX'),
('Luis Fernandez', 'luis.fernandez@ejemplo.ar', 'AR'),
('Carmen Lopez', 'carmen.lopez@ejemplo.cl', 'CL'),
('Miguel Santos', 'miguel.santos@ejemplo.co', 'CO'),
('Isabella Chen', 'isabella.chen@ejemplo.pe', 'PE'),
('Erik Anderson', 'erik.anderson@ejemplo.se', 'SE'),
('Lars Nielsen', 'lars.nielsen@ejemplo.no', 'NO');

-- Inserción de 20 facturas en invoices
INSERT INTO public.invoices (customer_id, invoice_date, total_amount) VALUES
(1, '2025-09-15', 1098.98),   
(2, '2025-09-16', 1299.00),   
(3, '2025-09-17', 629.76),    
(4, '2025-09-18', 889.98),   
(5, '2025-09-19', 499.00),   
(6, '2025-09-20', 493.99),   
(7, '2025-09-21', 824.50),   
(8, '2025-09-22', 329.99),   
(9, '2025-09-23', 268.97),    
(10, '2025-09-24', 135.49),   
(11, '2025-09-25', 1398.00),  
(12, '2025-09-26', 699.98),   
(13, '2025-09-27', 229.38),   
(14, '2025-09-28', 1299.00),  
(15, '2025-09-29', 929.97),   
(16, '2025-09-30', 693.99),   
(17, '2025-09-01', 799.00),   
(18, '2025-09-02', 672.73),   
(19, '2025-09-03', 243.98),   
(20, '2025-09-04', 116.99);  

-- Inserción de líneas de factura en invoice_lines
INSERT INTO public.invoice_lines (invoice_id, product_id, quantity, unit_price, line_total) VALUES
(1, 1, 1, 699.00, 699.00),
(1, 3, 2, 199.99, 399.98),
(2, 2, 1, 1299.00, 1299.00),
(3, 5, 1, 499.99, 499.99),
(3, 10, 3, 29.99, 89.97),
(3, 16, 2, 19.90, 39.80),
(4, 4, 1, 849.99, 849.99),
(4, 20, 1, 39.99, 39.99),
(5, 6, 1, 499.00, 499.00),
(6, 7, 2, 149.50, 299.00),
(6, 11, 1, 45.00, 45.00),
(6, 18, 1, 149.99, 149.99),
(7, 8, 1, 799.00, 799.00),
(7, 13, 2, 12.75, 25.50),
(8, 9, 1, 329.99, 329.99),
(9, 12, 1, 89.99, 89.99),
(9, 14, 2, 24.99, 49.98),
(9, 19, 1, 129.00, 129.00),
(10, 15, 3, 18.50, 55.50),
(10, 17, 1, 79.99, 79.99),
(11, 1, 2, 699.00, 1398.00),
(12, 3, 1, 199.99, 199.99),
(12, 5, 1, 499.99, 499.99),
(13, 7, 1, 149.50, 149.50),
(13, 10, 2, 29.99, 59.98),
(13, 16, 1, 19.90, 19.90),
(14, 2, 1, 1299.00, 1299.00),
(15, 4, 1, 849.99, 849.99),
(15, 20, 2, 39.99, 79.98),
(16, 6, 1, 499.00, 499.00),
(16, 11, 1, 45.00, 45.00),
(16, 18, 1, 149.99, 149.99),
(17, 8, 1, 799.00, 799.00),
(18, 9, 2, 329.99, 659.98),
(18, 13, 1, 12.75, 12.75),
(19, 12, 1, 89.99, 89.99),
(19, 14, 1, 24.99, 24.99),
(19, 19, 1, 129.00, 129.00),
(20, 15, 2, 18.50, 37.00),
(20, 17, 1, 79.99, 79.99);

--====================================Función RPC====================================

create or replace function public.create_invoice(
    customer_id bigint,
    items jsonb
)
returns jsonb
language plpgsql
security invoker
as $$
declare
    invoice_id bigint;
    total numeric(14,2) := 0;
    item jsonb;
    product_id bigint;
    quantity numeric(12,2);
    unit_price numeric(12,2);
    line_total numeric(14,2);
    lines jsonb := '[]'::jsonb;
    line_rec jsonb;
    missing_products bigint[];
begin
    ----- VALIDACIONES ------
    -- validar items
    if items is null then
        raise exception 'items no puede ser null';
    end if;
    if jsonb_typeof(items) <> 'array' or jsonb_array_length(items) = 0 then
        raise exception 'items debe ser un array no vacío';
    end if;

    -- validar que el customer existe y es accesible
    perform 1 from public.customers c where c.id = customer_id;
    if not found then
        raise exception 'customer % no existe o no es accesible', customer_id;
    end if;

    -- validar que todos los product_id del JSON existen y son accesibles
    with distinct_pids as ( -- Se guardan los ids en el alias distinct_pids
        select distinct (elem->>'product_id')::bigint as product_id -- distinct hace que si se repiten los ids, no se guarden los repetidos
        from jsonb_array_elements(items) elem
        where elem ? 'product_id' --toma los items que contengan product_id
    )
    select array_agg(d.product_id) --toma los d.product_id y los guarda en un array en la variable missing_products
    into missing_products
    from distinct_pids d
    left join public.products p on p.id = d.product_id
    where p.id is null; --Los p.id que tienen null se guardan (no hubo coincidencias)

    if missing_products is not null then
        raise exception 'los siguientes product_id no existen o no son accesibles: %', missing_products;
    end if;

    ----- PROCESAMIENTO ------
    for item in select * from jsonb_array_elements(items) loop
        begin
            product_id := (item->>'product_id')::bigint;
        exception when others then
            raise exception 'product_id inválido o ausente en item: %', item;
        end;

        begin
            quantity := (item->>'quantity')::numeric;
        exception when others then -- Cubre cualquier error que ocurra en el begin
            raise exception 'quantity inválida o ausente para product %', product_id;
        end;

        if quantity <= 0 then
            raise exception 'quantity debe ser mayor que 0 para product %', product_id;
        end if;

        -- si trae unit_price lo usamos, si no lo tomamos de products
        if (item ? 'unit_price') then
            begin
                unit_price := (item->>'unit_price')::numeric;
            exception when others then
                raise exception 'unit_price inválido para product %', product_id;
            end;
            if unit_price < 0 then
                raise exception 'unit_price no puede ser negativo para product %', product_id;
            end if;
        else
            select p.unit_price
            into unit_price
            from public.products p
            where p.id = product_id;

            if not found then
                raise exception 'producto % no existe o no es accesible', product_id;
            end if;
        end if;

        line_total := round(quantity * unit_price, 2); --redondea a dos decimales para la moneda
        total := round(total + line_total, 2);

        line_rec := jsonb_build_object( --se guarda el item
            'product_id', product_id,
            'quantity', quantity,
            'unit_price', unit_price,
            'line_total', line_total
        );

        lines := lines || jsonb_build_array(line_rec); -- se crea un json lines y se concatena el line_rec creado al final del json
    end loop;

    ----- INSERSIONES ------
    -- insertar invoice
    insert into public.invoices (customer_id, total_amount)
    values (customer_id, total)
    returning id into invoice_id; -- Devuelve el id de la factura creada y se guarda en invoice_id

    -- insertar líneas
    for item in select * from jsonb_array_elements(lines) loop
        insert into public.invoice_lines (
            invoice_id,
            product_id,
            quantity,
            unit_price,
            line_total
        )
        values (
            invoice_id,
            (item->>'product_id')::bigint,
            (item->>'quantity')::numeric,
            (item->>'unit_price')::numeric,
            (item->>'line_total')::numeric
        );
    end loop;

    return jsonb_build_object(
        'invoice_id', invoice_id,
        'customer_id', customer_id,
        'total_amount', total,
        'lines', lines
    );
exception
    when others then
        raise;
end;
$$;

