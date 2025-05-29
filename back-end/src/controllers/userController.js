//Controlador usuario
import { LoginService, validateToken } from "../services/userService.js"

export const LoginController = async (req, res) => {
  try {
    const user = { email: req.body.email, pwd: req.body.pwd };
    const response = await LoginService(user);
    res.status(200).json(response);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

export const verifyTokenController = async (req, res) => {
  try {
    const token = req.body.token;
    const response = await validateToken(token);
    res.status(200).json(response);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};