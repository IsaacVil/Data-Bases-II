const express = require('express');
const productSchema = require('../models/product');
const router = express.Router();

/**
 * @openapi
 * components:
 *   schemas:
 *     ProductInput:
 *       type: object
 *       required:
 *         - sku
 *         - name
 *         - category
 *         - unit
 *         - price
 *         - stock
 *       properties:
 *         sku:
 *           type: string
 *         name:
 *           type: string
 *         brand:
 *           type: string
 *         category:
 *           type: string
 *         unit:
 *           type: string
 *         price:
 *           type: number
 *         cost:
 *           type: number
 *         stock:
 *           type: number
 *         minStock:
 *           type: number
 *         location:
 *           type: string
 *         supplierId:
 *           type: string
 *         tags:
 *           type: array
 *           items:
 *             type: string
 *         imageURL:
 *           type: string
 *         active:
 *           type: boolean
 *         attributes:
 *           type: array
 *           items:
 *             type: object
 *             properties:
 *               key:
 *                 type: string
 *               value:
 *                 type: string
 *       example:
 *         sku: "P001"
 *         name: "Producto 1"
 *         brand: "Marca A"
 *         category: "Categoria X"
 *         unit: "kg"
 *         price: 12.5
 *         stock: 100
 *         minStock: 10
 *         location: "Almacen 1"
 *         supplierId: "S001"
 *         tags: ["tag1", "tag2"]
 *         imageURL: "http://example.com/image.jpg"
 *         active: true
 *         attributes: [{key: "Color", value: "Rojo"}]
 *
 *     Product:
 *       allOf:
 *         - $ref: '#/components/schemas/ProductInput'
 *         - type: object
 *           properties:
 *             _id:
 *               type: string
 *             createdAt:
 *               type: string
 *               format: date-time
 *             updatedAt:
 *               type: string
 *               format: date-time
 *
 *     ProductUpdate:
 *       type: object
 *       properties:
 *         sku:
 *           type: string
 *         name:
 *           type: string
 *         brand:
 *           type: string
 *         category:
 *           type: string
 *         unit:
 *           type: string
 *         price:
 *           type: number
 *         cost:
 *           type: number
 *         stock:
 *           type: number
 *         minStock:
 *           type: number
 *         location:
 *           type: string
 *         supplierId:
 *           type: string
 *         tags:
 *           type: array
 *           items:
 *             type: string
 *         imageURL:
 *           type: string
 *         active:
 *           type: boolean
 *         attributes:
 *           type: array
 *           items:
 *             type: object
 *             properties:
 *               key:
 *                 type: string
 *               value:
 *                 type: string
 *
 *     UpdateResult:
 *       type: object
 *       properties:
 *         acknowledged:
 *           type: boolean
 *         matchedCount:
 *           type: integer
 *         modifiedCount:
 *           type: integer
 *         upsertedCount:
 *           type: integer
 *         upsertedId:
 *           nullable: true
 *
 *     DeleteResult:
 *       type: object
 *       properties:
 *         acknowledged:
 *           type: boolean
 *         deletedCount:
 *           type: integer
 *
 *     Error:
 *       type: object
 *       properties:
 *         message:
 *           type: string
 *
 */




/**
 * @openapi
 * /api/products:
 *   post:
 *     summary: Crear un nuevo producto
 *     tags: [Products]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/ProductInput'
 *     responses:
 *       201:
 *         description: Producto creado exitosamente
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ProductInput'
 *       400:
 *         description: Bad request
 *       500:
 *         description: Error del servidor
 */




router.post('/products',
    async (req, res) => {
        const product = productSchema(req.body);
        product.save()
        .then((result) => {res.status(201).json(result)})
        .catch((err) => {res.status(500).json({ message: err.message || "algo paso mal en el post"})});
    }
);


/**
 * @openapi
 * /api/products:
 *   get:
 *     summary: Listar productos con filtros y paginación
 *     tags: [Products]
 *     parameters:
 *       - in: query
 *         name: q
 *         schema:
 *           type: string
 *         description: Texto para buscar en name, brand o category
 *       - in: query
 *         name: minstockAlert
 *         schema:
 *           type: boolean
 *         description: Si es true, filtra productos con stock > minStock
 *       - in: query
 *         name: limit
 *         schema:
 *           type: integer
 *         description: Limite de resultados
 *       - in: query
 *         name: skip
 *         schema:
 *           type: integer
 *         description: Cantidad de resultados a omitir (paginación)
 *     responses:
 *       200:
 *         description: Lista de productos
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/ProductInput'
 *       500:
 *         description: Error del servidor
 */




router.get('/products',
    async (req, res) => {
        try{
            const {q, minstockAlert, limit, skip} = req.query; //en query quedan los filtros
            const filter = {};
            if(q){
                filter.$or = 
                [
                    {name: {$regex: q, $options: "i"}},
                    {brand: {$regex: q, $options: "i"}},
                    {category: {$regex: q, $options: "i"}}
                ];
            }
            //poner lo de minstockAlert como true o false para activar o desactivar
            if(minstockAlert == 'true'){
                filter.$expr = { $gte: ["$stock", "$minStock"]}; //agregacion ($expr) donde  $gt es mayor que (stock > minstock)
            }
            const limits = Number(limit) || 0;
            const skips = Number(skip) || 0;
            productSchema.find(filter).skip(skips).limit(limits)
            .then((data) => {res.status(200).json(data)})
            .catch((err) => {res.status(500).json(err || "no se encontro")});
        }
        catch(err){
            res.status(500).json({ message: err.message || "algo paso mal en el get"});
            return;
        }
    }
)

/**
 * @openapi
 * /api/products/{id}:
 *   get:
 *     summary: Obtener un producto por ID
 *     tags: [Products]
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *         description: ID del producto
 *     responses:
 *       200:
 *         description: Producto encontrado
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ProductInput'
 *       404:
 *         description: Producto no encontrado
 *       500:
 *         description: Error del servidor
 */


router.get('/products/:id',
    async (req, res) => {
        try{
            const {id} = req.params;
            productSchema.findById(id)
            .then((data) => {res.status(200).json(data)})
            .catch((err) => {res.status(500).json(err || "no se encontro")});
        }
        catch(err){
            res.status(500).json({ message: err.message || "algo paso mal en el get"});
            return;
        }
    }
)

/**
 * @openapi
 * /api/products/{id}/adjust-stock:
 *   patch:
 *     summary: Ajustar el stock de un producto
 *     tags: [Products]
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *         description: ID del producto
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - stock
 *             properties:
 *               stock:
 *                 type: number
 *                 description: Nueva cantidad de stock
 *     responses:
 *       200:
 *         description: Stock ajustado
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/UpdateResult'
 *       404:
 *         description: Producto no encontrado
 *       500:
 *         description: Error del servidor
 */

router.patch('/products/:id/adjust-stock',
    async (req, res) => {
        try{
            const { id } = req.params; 
            const {stock} = req.body;
            const cantidad = Number(stock);
            if(!Number.isFinite(cantidad))
            {
                res.status(500).json({message: err.message || "Stock Invalido"});
                return; //Esto evita continue la ejecucion;
            }
            const producto = await productSchema.findById(id);
            if (!producto) {
                res.status(404).json({ message: "Producto inexistente" });
                return;
            }
            productSchema
                .updateOne({_id: id}, 
                    {$set: {stock: cantidad}}
                )
                .then((data) => {
                    res.json(data);
                })
                .catch((err) => {
                    res.status(500).json({message: err.message || "error"});
                });
        }
        catch(err){
            res.status(500).json({ message: err.message || "algo paso mal en el patch"});
            return;
        }
    }
);

/**
 * @openapi
 * /api/products/{id}:
 *   patch:
 *     summary: Actualizar parcialmente un producto
 *     tags: [Products]
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *         description: ID del producto
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/ProductUpdate'
 *     responses:
 *       200:
 *         description: Producto actualizado
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/UpdateResult'
 *       404:
 *         description: Producto no encontrado
 *       500:
 *         description: Error del servidor
 */

router.patch('/products/:id',
    async (req, res) => {
        try{
            const {id} = req.params;
            const producto = await productSchema.findById(id);
            if (!producto) {
                res.status(404).json({ message: "Producto inexistente" });
                return;
            }
            productSchema
                .updateOne({_id: id}, 
                    {$set: req.body},
                    {runValidators : true}
                )
                .then((data) => {
                    res.json(data);
                })
                .catch((err) => {
                    res.status(500).json({message: err.message || "error"});
                });
        }
        catch(err){
            res.status(500).json({ message: err.message || "algo paso mal en el patch"});
            return;
        }
    }
);

/**
 * @openapi
 * /api/products/{id}:
 *   delete:
 *     summary: Eliminar un producto
 *     tags: [Products]
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *         description: ID del producto
 *     responses:
 *       200:
 *         description: Producto eliminado
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/DeleteResult'
 *       404:
 *         description: Producto no encontrado
 *       500:
 *         description: Error del servidor
 */

router.delete('/products/:id',
    async (req, res) => {
        try{
            const {id} = req.params;
            productSchema.deleteOne({_id: id})
            .then((data) => {res.status(200).json(data)})
            .catch((err) => {res.status(500).json({message: err.message || "No se encontro"})});
        }
        catch(err){
            res.status(500).json({ message: err.message || "algo paso mal en el patch"});
            return;
        }
    }
);

module.exports = router;