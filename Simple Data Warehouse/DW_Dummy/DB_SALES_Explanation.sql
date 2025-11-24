-- OINV: el encabezado de la factura
SELECT * FROM OINV

-- PK DocEntry
-- DocNum es el numero de factura visible al cliente
-- DocType I es inventarios y S servicios
-- CardCode código de cliente
-- DocTotal y VatSum son el monto de la factura y su IVA en colones
-- DocTotalFC y VatSumFC son el monto de la factura y su IVA en dolares
-- slpCode salespersonCode es el vendedor

-- INV1: detalle de la factura

SELECT * FROM INV1
-- PK DocEntry, LineNum
--itemCode es FK a productos OITM

-------------------------------------------------------------------------------------------------
-- NOTAS DE CREDITO: deberian intenpretarse como negativa
--ORIN: notas de credito, son devoluciones, esta es el encabezado
--RIN1 detalle de nota de credito
SELECT * FROM ORIN;
SELECT * FROM RIN1;


-------------------------------------------------------------------------------------------------
-- CIENTES y Proveedores: OCRD
-- CardType C es un cliente, S proveedor-supplier
SELECT * FROM OCRD --where CardCode = 'V1010'

-- ZONAS que se pega con clientes por FK U_Zona
SELECT * FROM [dbo].[ZONAS]

-------------------------------------------------------------------------------------------------
-- ITEM o PRODUCTOS: OITM
-- u_mARCA ES FK se pega con la tabla MARCAS
-- OnHand es la exitencia total en la empresa para ese producto
-- CardCode es el codigo de proveedor se pega OCRD
SELECT * FROM OITM

-- MARCAS
SELECT * FROM MARCAS

-------------------------------------------------------------------------------------------------
-- OCRY
SELECT * FROM OCRY

-------------------------------------------------------------------------------------------------
--OSLP son los vendedores, SLP es salesPerson
-- Se pega con OINV y ORIN 
SELECT * FROM OSLP

-------------------------------------------------------------------------------------------------
-- INVENTARIOS POR BODEGA
-- OITW Item in warehouse
-- AvgPrice lo que me cuesta comprar ese producto
-- PK ItemCode + WhsCode
SELECT * FROM [dbo].[OITW]

-- Talba maestro de almacenes OWHS Object Warehouse
-- se pega con OITW por whsCode
SELECT * FROM [dbo].[OWHS]




