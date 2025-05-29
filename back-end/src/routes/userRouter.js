//Rutas de usuario
import { LoginController, verifyTokenController } from '../controllers/userController.js';
import express from 'express';

const userRouter = express.Router();

userRouter.post('/login', LoginController);
userRouter.post('/validateToken', verifyTokenController);

export default userRouter;