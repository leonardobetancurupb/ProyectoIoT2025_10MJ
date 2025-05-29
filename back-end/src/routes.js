import express from 'express';
import sensorRouter from './routes/sensorRouter.js';
import userRouter from './routes/userRouter.js';

const router = express.Router();

router.use('/api/sensors', sensorRouter);
router.use('/api/users', userRouter);

export default router;