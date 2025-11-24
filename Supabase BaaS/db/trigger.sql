CREATE OR REPLACE FUNCTION validacion_invoice_line()
RETURNS TRIGGER AS $$
DECLARE
    precioActual numeric(12,2);
BEGIN
    -- Utilizamos NEW. para obtener el id del producto que se está insertando
    SELECT unit_price INTO precioActual
    FROM public.products 
    WHERE id = NEW.product_id;

    -- Si no se encuentra el producto, lanzar error
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Producto con id % no encontrado', NEW.product_id;
    END IF;

    -- Validar que el unit_price sea igual al precio actual del producto
    IF NEW.unit_price != precioActual THEN
        RAISE EXCEPTION 'Trigger: El precio unitario (%) no coincide con el precio actual del producto (%)', NEW.unit_price, precioActual;
    END IF;

    -- Validar que line_total sea igual a quantity * unit_price
    IF NEW.line_total != (NEW.quantity * NEW.unit_price) THEN
        RAISE EXCEPTION 'Trigger: El total de línea (%) no coincide con quantity (%) * unit_price (%)', NEW.line_total, NEW.quantity, NEW.unit_price;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql; -- Esta línea nos permite utilizar instrucciones como IF

-- Creamos el trigger y le asignamos la función 
CREATE TRIGGER triggerValidacionInvoiceLines
    BEFORE INSERT OR UPDATE ON public.invoice_lines
    FOR EACH ROW
    EXECUTE FUNCTION validacion_invoice_line();

-- Esta inserción debe fallar
INSERT INTO public.invoice_lines (invoice_id, product_id, quantity, unit_price, line_total)
VALUES (1, 1, 1, 600.00, 600.00);

-- Esta inserción si sirve
INSERT INTO public.invoice_lines (invoice_id, product_id, quantity, unit_price, line_total)
VALUES (1, 1, 2, 699.00, 1398.00);
