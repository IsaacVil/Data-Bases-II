// Natalia Orozco Delgado (2024099161)
// Isaac Villalobos Bonilla (...)

db.Productos.drop();
db.createCollection("Productos");

db.Productos.insertMany([
 { sku:"P001", nombre:"Martillo Pro Acero", categoria:"Herramientas", precio:7500, stock:20, creadoEn:ISODate("2025-03-01T10:00:00Z") },
 { sku:"P002", nombre:"Destornillador Phillips #2", categoria:"Herramientas", precio:2500, stock:60, creadoEn:ISODate("2025-03-02T11:00:00Z") },
 { sku:"P003", nombre:"Llave Inglesa 10\"", categoria:"Herramientas", precio:5200, stock:35, creadoEn:ISODate("2025-03-03T09:00:00Z") },
 { sku:"P004", nombre:"Taladro Inalámbrico 18V", categoria:"Eléctricas", precio:45000, stock:8, creadoEn:ISODate("2025-03-04T12:00:00Z") },
 { sku:"P005", nombre:"Brocas para Metal (Juego 13p)", categoria:"Eléctricas", precio:9800, stock:15, creadoEn:ISODate("2025-03-05T08:30:00Z") },
 { sku:"P006", nombre:"Sierra Circular 7-1/4\"", categoria:"Eléctricas", precio:68500, stock:5, creadoEn:ISODate("2025-03-06T14:00:00Z") },
 { sku:"P007", nombre:"Guantes Anticorte Talla L", categoria:"Seguridad", precio:3200, stock:50, creadoEn:ISODate("2025-03-07T10:45:00Z") },
 { sku:"P008", nombre:"Lentes de Seguridad Pro", categoria:"Seguridad", precio:2900, stock:70, creadoEn:ISODate("2025-03-08T13:20:00Z") },
 { sku:"P009", nombre:"Casco de Seguridad Azul", categoria:"Seguridad", precio:8200, stock:18, creadoEn:ISODate("2025-03-09T09:15:00Z") },
 { sku:"P010", nombre:"Pintura Látex Interior Blanca 1 Gal", categoria:"Pinturas", precio:16500, stock:25, creadoEn:ISODate("2025-03-10T15:00:00Z") },
 { sku:"P011", nombre:"Rodillo de Pintura 9\" Antigota", categoria:"Pinturas", precio:4200, stock:40, creadoEn:ISODate("2025-03-11T08:00:00Z") },
 { sku:"P012", nombre:"Brocha 2\" Cerdas Naturales", categoria:"Pinturas", precio:2100, stock:80, creadoEn:ISODate("2025-03-12T17:00:00Z") }
]);


// Parte A: Consultas básicas 
console.log("\n=== Consulta: Mostrar todos los productos con solo sku, nombre y precio.")
printjson(
    db.Productos.find({}, {_id:0, sku:1, nombre:1, precio:1}).toArray()
);

console.log("\n=== Consulta: Productos con precio mayor a 10,000 CRC ordenados descendentemente.")
printjson(
    db.Productos.find({precio: {$gt: 10000}}).sort({precio: -1}).toArray()
);

console.log("\n=== Consulta: Productos de la categoría Seguridad o Pinturas.")
printjson(
   db.Productos.find({$or: [{categoria: "Seguridad"}, {categoria: "Pinturas"}]}).toArray()
);

console.log("\n=== Consulta: Mostrar todos los productos con stock entre 10 y 30.")
printjson(
    db.Productos.find({ stock: {$lt: 30, $gt: 10} }).toArray()
);

console.log("\n=== Consulta: Mostrar todos los productos cuyo nombre empiece con la letra P (sin importar mayúsculas o minúsculas)")
printjson(
    db.Productos.find({ nombre: /^P/i }).toArray()
);

console.log("\n=== Consulta: Mostrar paginacion mostrando 5 productos despues de saltar 3, ordenados por nombre.")
printjson(
    db.Productos.find().sort({nombre: 1}).skip(3).limit(5).toArray()
);


// Parte B: Updates
console.log("\n=== Update: Cambiar el precio de un producto específico a un nuevo valor")
db.Productos.updateOne({sku: "P001"}, {$set: {precio: 9000}});
printjson(
    db.Productos.findOne({sku: "P001"})
);

console.log("\n=== Update: Incrementar el stock de un producto en una cantidad determinada")
db.Productos.updateOne({sku: "P001"}, {$inc: {stock: 7}});
printjson(
    db.Productos.findOne({sku: "P001"})
);

console.log("\n=== Consulta: Agregar un campo tags a todos los productos.")
printjson(
    db.Productos.updateMany(
        { tags: { $exists: false } },
        { $set: {tags: ["herramienta", "electrica"] } }
    )
);

console.log("\n=== Consulta: Normalizar el nombre de un producto (por ejemplo cambiar 'IA' por 'Inteligencia Artificial')")
printjson(
    db.Productos.updateMany({nombre: "Brocha 2\" Cerdas Naturales"}, {$set: {nombre: "Brocha con Cerdas Naturales"}})
);

// Parte C: Upsert
console.log("\n=== Consulta: Realizar un upsert sobre un producto por su sku. Si existe, actualizar el stock; si no existe, insertarlo con todos los datos.')")
printjson(
    db.Productos.updateOne({sku: "P013"}, {$set: {nombre: "palabra clave: brocha 22", precio: 200000, stock: 100}}, {upsert: true})
);

// Parte D: Deletes
console.log("\n=== Delete: Eliminar un producto específico por su sku")
db.Productos.deleteOne({sku: "P002"});
printjson(
    db.Productos.findOne({sku: "P002"})
);

console.log("\n=== Delete: Eliminar todos los productos con stock enor a 10 unidades")
db.Productos.deleteMany({stock: {$lt: 10}});
printjson(
   db.Productos.find({stock: {$lt: 10}})
);

// Parte E: Agregaciones
console.log("\n=== Agregación: Calcular el precio promedio, mínimo y máximo de por categoría")
printjson(
    db.Productos.aggregate([{ $group: {_id: "$categoria", promedio: {$avg: "$precio"}, minimo: {$min: "$precio"}, maximo: {$max: "$precio"}}}]).toArray()
);

console.log("\n=== Agregación: Calcular el valor total del inventario por categoría (precio * stock)")
printjson(
    db.Productos.aggregate([{$project: {_id : 0, categoria: 1, valorInventario: {$multiply: ["$precio", "$stock"]}}}, { $group: { _id: "$categoria", valorInventario: {$sum: "$valorInventario"}}}]).toArray()
);

console.log("\n=== Agregación: Mostrar el top 3 productos más caros")
printjson(
    db.Productos.aggregate([{$sort : {precio: -1}}, {$limit: 3}]).toArray()
);

// Parte E:  (4)
console.log("\n=== Consulta: Agrupar productos por categoría y contar total de productos por categoría.")
printjson(
    db.Productos.aggregate([        
        {$group: {
            _id: "$categoria",
            total: {$sum: 1}
        }}
      ])
);

// Parte E:  (5)
console.log("\n=== Consulta: Agrupar productos por rango de precio. Histograma")
printjson(
    db.Productos.aggregate([
        {
            $bucket: {
                groupBy: "$precio",
                boundaries: [0, 1000, 5000, 10000, 25000, 100000],
                default: "Fuera De Rango",
                output: { cantidad: { $sum: 1 }}
            }
        }
      ])
);

// Parte E:  (6)
console.log("\n=== Consulta: Agrupar productos por rango de precio automatico. Histograma")
printjson(
    db.Productos.aggregate([
        {
            $bucketAuto: {
                groupBy: "$precio",
                buckets: 3,
                output: {
                    count: { $sum: 1 }
                }
            }
        }
      ])
);

//VERIFICAR (puedo usar slice y cosas distintas?)
console.log("\n=== Agregaciones: Obtener los 3 productos más caros dentro de cada categoría (ranking interno)")
printjson(
    db.Productos.aggregate([{$sort: {precio: -1}}, {$group: {_id: "$categoria", top: {$push: {nombre: "$nombre", precio: "$precio"}}}}, {$project: {top: {$slice: ["$top",3]}}}]).toArray()
);

//VERIFICAR (raro)
console.log("\n=== Agregaciones: Mostrar productos que contengan la palabra 'Pro' en su nombre y calcular su porcentaje en cada categoría.")
printjson(
    db.Productos.aggregate([{$group: {_id: "$categoria", total: {$sum:1}, pros: {$push: {$cond: [{$regexMatch: {input: "$nombre", regex: /Pro/}}, "$nombre", "$$REMOVE"]}}}}, {$project: {porcentajePro: {$multiply: [{$divide: [{$size: "$pros"}, "$total"]}, 100]}, pros:1}}]).toArray()
);

console.log("\n=== Agregaciones: Consultar productos creados dentro de un rango de fechas.")
printjson(
    db.Productos.aggregate([{$match: {creadoEn: {$gte: ISODate("2025-01-01"), $lte: ISODate("2025-03-09")}}}]).toArray()
);

// Parte E:  (10)
console.log("\n=== Consulta: Listar etiquetas unicas por categoría (si existe el campo tags).")
printjson(
    db.Productos.aggregate([
        { $match: { tags: { $exists: true } } },
        { $unwind: "$tags" },
        { $group: { _id: { categoria: "$categoria", tag: "$tags" }, count: { $sum: 1 } } },
        { $match: { count: 1 } }
    ])
);

// Parte E:  (11)
console.log("\n=== Consulta: Contar productos por palabras clave en el nombre")
printjson(
    db.Productos.aggregate([
        { $match: { nombre: /brocha/i } },
        { $count: "total de apariciones" }
    ])
);

// Parte E:  (12)
// VERIFICAR!!!!!!!!!!!!!!!!!! (PUEDO USAR UNA CONSTANTE?)
console.log("\n=== Agregaciones: Clasificar productos por costo conforme al promedio general de precio.")
const promedio = db.Productos.aggregate([
    { $group: { _id: null, promedio: { $avg: "$precio" } } }
]).toArray()[0].promedio;
printjson(
    db.Productos.aggregate([
        {
            $project: {
                nombre: 1,
                precio: 1,
                categoriaPrecio: {
                    $switch: {
                        branches: [
                            { case: { $gt: ["$precio", promedio] }, then: "Caro" },
                            { case: { $lt: ["$precio", promedio] }, then: "Barato" }
                        ],
                        default: "Promedio"
                    }
                }
            }
        },
        {
            $group: {
                _id: "$categoriaPrecio",
                productos: { $push: "$nombre" }
            }
        }
    ])
);

console.log("\n=== Agregaciones: Calcular el valor total de inventario agrupado por día de creación.")
printjson(
    db.Productos.aggregate([{$group: {_id: {$dateToString: { format: "%Y-%m-%d", date: "$creadoEn" }}, inventarioTotal: {$sum: "$stock"}}}]).toArray()
);

//VERIFICAR (resumen?)
console.log("\n=== Agregaciones: Generar un reporte múltiple con $facet que incluya: top 3 productos caros, resumen por categoría y productos con 'Pro'.")
printjson(
    db.Productos.aggregate([{$facet: { top3: [{$sort : {precio: -1}}, {$limit: 3}], resumenCategoria: [{$group: {_id: "$categoria", cantidad: {$sum: 1}}}], productosConPro: [ {$match: {nombre: {$regex: /Pro/}}}]}}]).toArray()
);

//VERIFICAR (estatico?)
console.log("\n=== Agregaciones: Clasificar productos por niveles de stock (Bajo, Medio, Alto).")
printjson(
    db.Productos.aggregate([{$bucket: {groupBy: "$stock", boundaries: [0, 20, 50, 100], default: "Fuera de rango", output: {productos: { $push: "$nombre" } }}}, {$project: {_id: 0, categoria: { $switch: {branches: [{ case: { $eq: ["$_id", 0] }, then: "Bajo" },{ case: { $eq: ["$_id", 20] }, then: "Medio" },{ case: { $eq: ["$_id", 50] }, then: "Alto" }], default: "Fuera de rango"}},productos: 1}}]).toArray()
);

// Parte E:  (16)
console.log("\n=== Consulta: Listar productos que contengan comillas en su nombre")
printjson(
    db.Productos.aggregate([
        { $match: { nombre: /[""]/i } }
    ]).toArray()
);

// Parte E:  (17)
console.log("\n=== Consulta: Mostrar catálogo resumido por categoría con los 5 productos más caros y nombres representativos. ")
printjson(
    db.Productos.aggregate([
        { $sort: { precio: -1 } },
        { $group: {
            _id: "$categoria",
            top: {
                $push: {
                    nombreDescriptivo: { $concat: ["Producto: ", "$nombre", " , pertenece a la categoria: ", "$categoria"] }
                }
            }
        }},
        { $project: {
            top: { $slice: ["$top", 5] }
        }}
    ]).toArray()
);

// Parte E:  (18)
console.log("\n=== Consulta: Crear un campo derivado precioConIVA (13%) y mostrarlo en un reporte")
printjson(
    db.Productos.aggregate([
        {
            $project: {
                _id: 0,
                nombre: 1,
                precio: 1,
                iva: { $multiply: ["$precio", 0.13] }
            }
        }
    ]).toArray()
);



