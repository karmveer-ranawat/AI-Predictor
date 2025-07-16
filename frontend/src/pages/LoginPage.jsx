// --- src/pages/LoginPage.jsx ---
import { useEffect, useState } from "react";
import axios from "../api/axios";

const LoginPage = () => {
  const [loginUrl, setLoginUrl] = useState("");

  useEffect(() => {
    const fetchLoginUrl = async () => {
      try {
        const res = await axios.get("/auth/login_url");
        setLoginUrl(res.data.login_url);
      } catch (err) {
        console.error("Failed to fetch login URL", err);
      }
    };
    fetchLoginUrl();
  }, []);

  const handleLogin = () => {
    window.location.href = loginUrl;
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-50">
      <button
        onClick={handleLogin}
        disabled={!loginUrl}
        className="px-6 py-3 bg-red-600 text-white text-lg font-semibold rounded-lg shadow hover:bg-red-700"
      >
        {loginUrl ? "Login with Kite" : "Loading..."}
      </button>
    </div>
  );
};

export default LoginPage;
