//Lógica para los usuarios (login)
import { signInWithEmailAndPassword } from 'firebase/auth'
import { auth } from '../db/firebase-config.js';
import {admin} from '../db/firebase-admin.js'

export const LoginService = async (user) => {

    try {

        const regexCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (!user.email) throw new Error("Please provide an email");
        if (!(regexCorreo.test(user.email))) throw new Error("Please insert a correct email");
        if (!user.pwd) throw new Error("Please provide a password");

        const response = await signInWithEmailAndPassword(auth, user.email, user.pwd);
        const token = await response.user.getIdToken();

        const decoded = await admin.auth().verifyIdToken(token);
        const exp = decoded.exp;
        return {
            success: true,
            user: {
                uid: response.user.uid,
                email: response.user.email,
            },
            token,
            expiresAt: exp,
        };

    } catch (error) {
        return {
            success: false,
            message: error.message
        }
    }

};

export const validateToken = async (token) => {

    try {

        const decodedToken = await admin.auth().verifyIdToken(token);
        return {
            success: true,
            uid: decodedToken.uid,
            email: decodedToken.email,
            decodedToken
        };

    } catch (error) {
        return {
            success: false,
            message: 'Invalid token',
            error
        };
    }

}