import { initializeApp } from "firebase/app";
import {getAuth} from 'firebase/auth'

const firebaseConfig = {
  apiKey: "AIzaSyA_CLnxwY-NqscJjHMRwv0TyegcqXS_vpM",
  authDomain: "iot-users.firebaseapp.com",
  projectId: "iot-users",
  storageBucket: "iot-users.firebasestorage.app",
  messagingSenderId: "124110470510",
  appId: "1:124110470510:web:3e72de55c94c3346a0557f",
  measurementId: "G-LH19VHV0Z9"
};

const firebaseApp = initializeApp(firebaseConfig);
export const auth = getAuth(firebaseApp);