import StockScannerPanel from "../components/StockScannerPanel";
import MLTabs from "../components/MLTabs";

const DashboardPage = () => (
  <div className="max-w-6xl mx-auto pt-10 px-4">
    <h1 className="text-3xl font-bold text-[#a83232] mb-8">Dashboard</h1>

    <div className="grid md:grid-cols-2 gap-10">
      <StockScannerPanel />   {/* left side */}
      <MLTabs />              {/* right side */}
    </div>
  </div>
);

export default DashboardPage;
