import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { registerApi } from "../api/auth";

function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      await registerApi(email, password);
      alert("Registered successfully. Please login.");
      navigate("/login", { replace: true });
    } catch {
      alert("Registration failed");
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-container">
        <h2>Register</h2>
        <p className="subtitle">Create your SME account</p>

        <input
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={handleRegister}>Register</button>

        <div className="auth-footer">
          Already registered? <Link to="/login">Login</Link>
        </div>
      </div>
    </div>
  );
}

export default RegisterPage;
