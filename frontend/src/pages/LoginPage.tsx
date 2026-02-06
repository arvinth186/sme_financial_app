import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { loginApi } from "../api/auth";
import { loginUser } from "../utils/auth";

function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const data = await loginApi(email, password);
      loginUser(data.access_token);
      navigate("/", { replace: true });
    } catch {
      alert("Invalid email or password");
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-container">
        <h2>Login</h2>
        <p className="subtitle">Access your financial dashboard</p>

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

        <button onClick={handleLogin}>Login</button>

        <div className="auth-footer">
          New user? <Link to="/register">Register</Link>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
