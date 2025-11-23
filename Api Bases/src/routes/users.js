const express = require('express');
const userSchema = require('../models/user');
const router = express.Router();

/**
 * @openapi
 * components:
 *   schemas:
 *     UserInput:
 *       type: object
 *       required:
 *         - name
 *         - age
 *         - email
 *         - password
 *       properties:
 *         name:
 *           type: string
 *           description: The name of the user
 *         age:
 *           type: integer
 *           format: int32
 *           description: The age of the user
 *         email:
 *           type: string
 *           format: email
 *           description: The email of the user
 *         password:
 *           type: string
 *           description: The password of the user
 *       example:
 *         name: John Doe
 *         age: 30
 *         email: john.doe@example.com
 *         password: securepassword
 *
 *     User:
 *       allOf:
 *         - $ref: '#/components/schemas/UserInput'
 *         - type: object
 *           properties:
 *             _id:
 *               type: string
 *               description: Mongo ObjectId
 *             createdAt:
 *               type: string
 *               format: date-time
 *             updatedAt:
 *               type: string
 *               format: date-time
 *
 *     UserUpdate:
 *       type: object
 *       description: Campos a actualizar (todos opcionales)
 *       properties:
 *         name:
 *           type: string
 *         age:
 *           type: integer
 *           format: int32
 *         email:
 *           type: string
 *           format: email
 *         password:
 *           type: string
 *
 *     UpdateResult:
 *       type: object
 *       properties:
 *         acknowledged:
 *           type: boolean
 *           example: true
 *         matchedCount:
 *           type: integer
 *           example: 1
 *         modifiedCount:
 *           type: integer
 *           example: 1
 *         upsertedCount:
 *           type: integer
 *           example: 0
 *         upsertedId:
 *           nullable: true
 *           example: null
 *
 *     DeleteResult:
 *       type: object
 *       properties:
 *         acknowledged:
 *           type: boolean
 *           example: true
 *         deletedCount:
 *           type: integer
 *           example: 1
 *
 *     Error:
 *       type: object
 *       properties:
 *         message:
 *           type: string
 *           example: User not found
 */


/**
 * @openapi
 * /api/users:
 *   post:
 *     summary: Create a new user
 *     tags: [Users]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/UserInput'
 *     responses:
 *       201:
 *         description: The user was successfully created
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/User'
 *       400:
 *         description: Bad request
 */


router.post('/Users', 
    async (req, res) => {
        console.log(req.body);
        console.log(req.headers);
        const user = userSchema(req.body);
        user
            .save()
            .then((result) => {res.status(201).json(result);
            })
            .catch((err) => {res.status(500).json({ message: err.message || "algo paso mal en el post"});
        });
    }
);

/**
 * @openapi
 * /api/users:
 *   get:
 *     summary: Get all users
 *     tags: [Users]
 *     responses:
 *       200:
 *         description: List of users
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/User'
 *       500:
 *         description: Server error
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Error'
 */

router.get('/Users',
    async (req, res) => {
        userSchema
            .find()
            .then((data) => {
                res.status(203).json(data);
            })
            .catch((err) => {
                res.status(500).json({message: err.message || "No se encontro"});
            });
    }
);

//filter?age=30&name=Isaac
//buscar los edad mayor que el age y contengan el name
router.get('/Users/filter',
    async(req, res) => {
        try{
            const {age, name} = req.query; //todos los filtros que van en la URL se llamara "query"
            // Esto es lo mismo que lo de arriba, se crea un json con el age y name asignados a esos campos, porque esa const es un json tmb
            //let variable = {
            //    age: req.query.age,
            //   name: req.query.name
            //}
            const filter = {};
            if (name){
                filter.name = new RegExp(String(name), 'i'); //String lo vuelve string y la i es para dejarlo case insensitive (no importa mayusculas)
                if(age) //Si no es undefined, ni 0 como ententero ni null (vease que es un string entonces si es 0 si pasa pero si es un 0 de verdad entonces no entra)
                {
                    const N = Number(age); //Convertimos la edad a entero
                    if(!Number.isFinite(N)) //Si el numero no es finito esta malo (puede ser que intento hacer un "hola" a numero y se cayo el N)
                    {
                        res.status(500).json({message: err.message || "Edad Invalida"});
                        return; //Esto evita continue la ejecucion;
                    }
                    filter.age = { $gt: N }; //o sea vamos a buscar mayor que n
                    console.log(filter);
                    const users = await userSchema.find(filter); //va a buscar conforme a las reglas que le mandamos en el filtro, con el find de mongo
                    res.json(users); //aqui devuelve a todo el json que trae todos lso usuarios que cumplen los filtros
                }
            }
            else 
            {
                res.status(500).json({message: err.message || "Nombre Invalida"});
            }
        }catch{
            res.status(500).json({message: err.message || "No se encontro"});
            return;
        }
    }
);

//solo cambia algo de todo
router.patch('/Users/:id',
    async (req, res) => {
        const {id} = req.params; //es una parametro que se dara antes de los ?name=pablo&age=19
        const {name, age, email, password} = req.body; //es body y no query pq viene del body no de lo de la URL
        userSchema
            .updateOne({_id: id}, { $set: {name, age, email, password}})
            .then((data) => {
                res.json(data);
            })
            .catch((err) => {
                res.status(500).json({message: err.message || "error"});
            });
    }
);

router.delete('/Users/:id',
    async (req, res) => {
        const {id} = req.params; //es una parametro que se dara antes de los ?name=pablo&age=19
        userSchema
            .deleteOne({_id: id})
            .then((data) => {
                res.json(data);
            })
            .catch((err) => {
                res.status(500).json({message: err.message || "error"});
            });
    }
);

router.get('/Users/:id',
    async (req, res) => {
        const {id} = req.params;
        userSchema
            .findById(id)
            .then((data) => {
                res.status(203).json(data);
            })
            .catch((err) => {
                res.status(500).json({message: err.message || "No se encontro"});
            });
    }
);

//esto le caeria encima a todo el json
router.put('/Users/:id/close',
    async (req, res) => {
        const {id} = req.params;
        userSchema
            .findById(id)
            .then((data) => {
                res.status(203).json(data); //Aqui se haria el query de updatear algo pero no volarselo al completo
            })
            .catch((err) => {
                res.status(500).json({message: err.message || "No se encontro"});
            });
    }
);


module.exports = router;
