import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../api/axios";

const TokenHandlerPage = () => {
  const navigate = useNavigate();
  const hasHandled = useRef(false); // ✅ new

  useEffect(() => {
    if (hasHandled.current) return; // ✅ prevent multiple fires
    hasHandled.current = true;

    const urlParams = new URLSearchParams(window.location.search);
    const requestToken = urlParams.get("request_token");

    if (requestToken) {
      axios
        .post("/auth/token", { request_token: requestToken })
        .then(() => {
          alert("✅ Login successful");
          navigate("/dashboard");
        })
        .catch((err) => {
          console.error(err);
          alert("❌ Login failed");
          navigate("/");
        });
    } else {
      alert("❌ No request token found");
      navigate("/");
    }
  }, [navigate]);

  return (
    <div className="flex justify-center items-center h-screen">
      <p className="text-gray-600 text-lg">Processing login...</p>
    </div>
  );
};

export default TokenHandlerPage;
