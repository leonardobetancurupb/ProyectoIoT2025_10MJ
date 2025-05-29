import admin from 'firebase-admin';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);

const serviceAccount = require('./private-key/iot-users-firebase-adminsdk-fbsvc-cb3521339a.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

export { admin };