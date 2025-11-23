//Required
    //Esta es la formula basica de un servidor con express
const express = require('express'); //este es como un import de una libreria.
const mongoose = require('mongoose'); //libreria para conectar con mongoDB
require('dotenv').config(); //para leer las variables de entorno desde un archivo .env !!!
const userRoutes = require('./routes/users'); //importo la ruta
const productRoutes = require('./routes/products');

const app = express(); //es la instancia de express
const PORT = process.env.PORT || 3000; //El puerto donde va a correr el servidor (esta en un .env por ser datos sensibles)

//Swagger (PARA DOCUMENTAR, BASTANTE BUENO)
const path = require("path"); //importamos esta libreria requerida
const swaggerUi = require("swagger-ui-express"); //importamos la ruta de express necesarias
const swaggerJsDoc = require("swagger-jsdoc"); //importamos para que soporte javascript documents 

    // Options (del swagger)
const swaggerOptions = {
  definition: {
    openapi: '3.0.3',
    info: { title: 'Taller API', version: '1.0.0' }, //Nombre del api en el titulo (Family Food Api) y esa version es la version del swagger
    servers: [{ url: 'http://localhost:3000' }], //Aca seria una variable de ambiente para no descubrir donde esta el server como la const port
  },
  apis: [    
    path.resolve(__dirname, './routes/users.js'),
    path.resolve(__dirname, './routes/products.js')
  ], //
};
const swaggerSpec = swaggerJsDoc(swaggerOptions); //Le pasamos el json de configuracion



//Middlewares: llamados antes de llegar a las rutas
app.use(express.json()); //! para que el server entienda json
app.use('/api', userRoutes); //le digo a express que use las rutas que importamos antes
app.use('/api', productRoutes);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec)); //le decimos a express que use las rutas de swagger

//Routes
app.get('/', (req, res) => { //req = request (lo que llega) y res = response (lo que se envia)
    //TODO: todo lo que quiero hacer
    res.send('Hello World!'); //envia un mensaje al navegador
});

mongoose.connect(process.env.MONGODB_URI) //conexion a la base de datos (la uri esta en un .env por ser datos sensibles)
    .then(() => { console.log("Connected to mongo"); })
    .catch((err) => { console.error("Error connecting to mongo", err); });

//Listen
    //Express esta escuchando en el puerto y luego dice en cual corre.
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT} ip: http://localhost:${PORT}`);
});

