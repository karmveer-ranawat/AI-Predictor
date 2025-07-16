import { Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import TokenHandlerPage from "./pages/TokenHandlerPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/kite-redirect" element={<TokenHandlerPage />} />
    </Routes>
  );
}

export default App;
