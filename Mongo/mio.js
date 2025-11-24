db.Productos.drop();
db.createCollection("Productos");

db.Productos.insertMany([
 { sku:"P001", nombre:"Martillo Pro Acero", categoria:"Herramientas", precio:7500, stock:20, creadoEn:ISODate("2025-03-01T10:00:00Z") },
 { sku:"P002", nombre:"Destornillador Phillips #2", categoria:"Herramientas", precio:2500, stock:60, creadoEn:ISODate("2025-03-02T11:00:00Z") },
 { sku:"P003", nombre:"Llave Inglesa 10\"", categoria:"Herramientas", precio:5200, stock:35, creadoEn:ISODate("2025-03-03T09:00:00Z") },
 { sku:"P004", nombre:"Taladro Inalámbrico 18V", categoria:"Eléctricas", precio:45000, stock:8, creadoEn:ISODate("2025-03-04T12:00:00Z") },
 { sku:"P005", nombre:"Brocas para Metal (Juego 13p)", categoria:"Eléctricas", precio:9800, stock:15, creadoEn:ISODate("2025-03-05T08:30:00Z") },
 { sku:"P006", nombre:"Sierra Circular 7-1/4\"", categoria:"Eléctricas", precio:68500, stock:5, creadoEn:ISODate("2025-03-06T14:00:00Z") },
  { sku:"P015", nombre:"Brocas para Metal (Juego 13p)", categoria:"Eléctricas", precio:9800, stock:15, creadoEn:ISODate("2025-03-05T08:30:00Z") },
 { sku:"P016", nombre:"Sierra Circular 7-1/4\"", categoria:"Eléctricas", precio:68500, stock:5, creadoEn:ISODate("2025-03-06T14:00:00Z") },
 { sku:"P007", nombre:"Guantes Anticorte Talla L", categoria:"Seguridad", precio:3200, stock:50, creadoEn:ISODate("2025-03-07T10:45:00Z") },
 { sku:"P008", nombre:"Lentes de Seguridad Pro", categoria:"Seguridad", precio:2900, stock:70, creadoEn:ISODate("2025-03-08T13:20:00Z") },
 { sku:"P009", nombre:"Casco de Seguridad Azul", categoria:"Seguridad", precio:8200, stock:18, creadoEn:ISODate("2025-03-09T09:15:00Z") },
 { sku:"P010", nombre:"Pintura Látex Interior Blanca 1 Gal", categoria:"Pinturas", precio:16500, stock:25, creadoEn:ISODate("2025-03-10T15:00:00Z") },
 { sku:"P011", nombre:"Rodillo de Pintura 9\" Antigota", categoria:"Pinturas", precio:4200, stock:40, creadoEn:ISODate("2025-03-11T08:00:00Z") },
 { sku:"P012", nombre:"Brocha 2\" Cerdas Naturales", categoria:"Pinturas", precio:2100, stock:80, tags: ["Brochas"], creadoEn:ISODate("2025-03-12T17:00:00Z") }
]);

// Parte A: Consultas básicas (4,5,6)

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

// Parte B:  (3,4)

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

// Parte C:  (1)
console.log("\n=== Consulta: Realizar un upsert sobre un producto por su sku. Si existe, actualizar el stock; si no existe, insertarlo con todos los datos.')")
printjson(
    db.Productos.updateOne({sku: "P013"}, {$set: {nombre: "palabra clave: brocha 22", precio: 200000, stock: 100}}, {upsert: true})
);

// Parte E:  (4,5,6,10,11,12,16,17,18)

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
console.log("\n=== Consulta: ")
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