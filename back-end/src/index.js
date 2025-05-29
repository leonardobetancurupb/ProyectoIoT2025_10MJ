import express from 'express';
import cors from 'cors';
import routes from './routes.js';

const app = express()
app.use(express.json())

const port = 3000

app.use(cors({
    origin: '*', 
}))  

app.get('/ping', (_req, res) =>{
    console.log('someone pinged here!!')
    res.send('pong')
})

//Uso de las rutas
app.use('/', routes)

app.listen(port, () =>{
    console.log(`Sever running on port ${port}`)

})