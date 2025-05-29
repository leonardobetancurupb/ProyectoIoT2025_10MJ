import { useState } from 'react';
import "./LoginPage.css";
import upb from "../../assets/logo_upb.png";
import { Link } from "react-router-dom";
import { userLogin } from "../../api/user/user.js";
import Swal from 'sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';

const LoginPage = () => {
  const [usuario, setUsuario] = useState({email: '', pwd: '' });

  const manejarCambio = e => {
    setUsuario({ ...usuario, [e.target.name]: e.target.value });
  };

  const manejarEnvio = async e => {
    e.preventDefault();
    try {
      const response = await userLogin(usuario);
      const data = response.data;
      if(data.success){
        Swal.fire({
            title: '¡Bienvenido!',
            text: 'Has iniciado sección correctamente.',
            icon: 'success',
            confirmButtonText: 'OK'
        })
        .then(() => { 
          localStorage.setItem('UserToken',  data.token);
          window.location.href = `/overview`;
        });

      }else{
        Swal.fire({
            title: '¡Lo sentimos!',
            text: 'Credenciales incorrectas.',
            icon: 'error',
            confirmButtonText: 'OK'
        });        
      }
    } catch (error) {
      console.error('Error en el login:', error);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <img src={upb} alt="UPB Logo" className="login-logo" />
        <h2 className="login-title">Welcome Back</h2>
        <p className="login-subtitle">Sign in to continue to your dashboard</p>
        <form className="login-form" onSubmit={manejarEnvio}>
          <input type="email" name='email' placeholder="Email" className="login-input" required onChange={manejarCambio}/>
          <input type="password" name="pwd" placeholder="Password" className="login-input" required onChange={manejarCambio} />
          <button type="submit" className="login-button">Login</button>
        </form>
        <p className="login-footer">Don't have an account? <Link to="/register" className="Login-button"> Register </Link></p>
      </div>
    </div>
  );
};

export default LoginPage;
