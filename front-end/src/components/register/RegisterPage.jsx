import React from "react";
import "./RegisterPage.css";
import upb from "../../assets/logo_upb.png";
import { Link } from "react-router-dom";
const RegisterPage = () => {
  return (
    <div className="register-container">
      <div className="register-card">
        <img src={upb} alt="UPB Logo" className="register-logo" />
        <h2 className="register-title">Welcome </h2>
        <p className="register-subtitle">Register in to continue to your dashboard</p>
        <form className="register-form">
          <input type="email" placeholder="Email" className="register-input" required />
          <input type="password" placeholder="Password" className="register-input" required />
          <input type="password" placeholder="Confirm Password" className="register-input" required />
          <button type="submit" className="register-button">Register</button> 
        </form>
      </div>
    </div>
  );
};

export default RegisterPage;
