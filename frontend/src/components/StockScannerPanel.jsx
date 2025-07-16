import { useEffect, useState } from "react";
import PredictionBox from "./PredictionBox";
import axios from "../api/axios";
// comment out if you don’t install lucide‑react
import { Search as SearchIcon } from "lucide-react";

const StockScannerPanel = () => {

    /* ───────── state ───────── */
    const [stocks, setStocks] = useState([]);
    const [filteredStocks, setFilteredStocks] = useState([]);
    const [selected, setSelected] = useState([]);
    const [search, setSearch] = useState("");
    const [scanType, setScanType] = useState("all");
    const [isScanning, setIsScanning] = useState(false);
    const [scanStatus, setScanStatus] = useState({});
    const [scanResults, setScanResults] = useState([]);
    const [showModal, setShowModal] = useState(false);

    const [summaryData, setSummaryData] = useState(null);
    const [showSummary, setShowSummary] = useState(false);

    /* ───────── fetch symbols once ───────── */
    useEffect(() => {
        const fetchSymbols = async () => {
        try {
            const res = await axios.get("/scanner/all_symbols");
            setStocks(res.data.symbols);
            setFilteredStocks(res.data.symbols);
        } catch (err) {
            console.error("Failed to fetch symbols", err);
        }
        };
        fetchSymbols();
    }, []);

    /* ───────── live search filter ───────── */
    useEffect(() => {
        setFilteredStocks(
        stocks.filter((s) => s.toLowerCase().includes(search.toLowerCase()))
        );
    }, [search, stocks]);

    /* ───────── helpers ───────── */
    const toggleSelection = (symbol) => {
        setSelected((prev) =>
        prev.includes(symbol) ? prev.filter((s) => s !== symbol) : [...prev, symbol]
        );
    };

    const viewSummary = async (symbol) => {
        try {
        const res = await axios.get(`/scanner/summary/${symbol}`);
        setSummaryData(res.data);
        setShowSummary(true);
        } catch {
        alert("No saved summary for " + symbol);
        }
    };

    const statusBadge = (status) => {
        if (status === "scanning")
        return <span className="text-yellow-600 text-xs">⏳</span>;
        if (status === "done")
        return <span className="text-green-600 text-xs">✅</span>;
        if (status === "error")
        return <span className="text-red-600 text-xs">❌</span>;
        return null;
    };

    /* ───────── run scanners ───────── */
    const runScannersOnSelected = async () => {
        if (!selected.length) return;
        setIsScanning(true);

        const statusMap = {};
        const results = [];

        for (const symbol of selected) {
        try {
            setScanStatus((p) => ({ ...p, [symbol]: "scanning" }));

            let res;
            if (scanType === "all") {
            res = await axios.get(`/scanner/scan_stock/${symbol}`);
            } else {
            res = await axios.get(
                `/scanner/scan_type_stock/${scanType}/${symbol}`
            );
            }
            results.push({ symbol, result: res.data[symbol] || {} });
            statusMap[symbol] = "done";
        } catch {
            statusMap[symbol] = "error";
            results.push({ symbol, result: { error: true } });
        }
        }

        setScanStatus((p) => ({ ...p, ...statusMap }));
        setScanResults(results);
        setShowModal(true);
        setIsScanning(false);
    };

    /* ───────── UI ───────── */
    return (
    <div className="w-full">
        {/* ── Panel heading ── */}
        <h2 className="text-xl font-semibold mb-4">Your Stocks</h2>

        {/* ── Search, dropdown & list card ── */}
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 shadow-sm space-y-3">
        {/* Search bar */}
        <div className="relative">
            <input
            className="w-full px-10 py-2 border border-gray-300 rounded-md bg-white focus:outline-none focus:ring-2 focus:ring-[#a83232]"
            placeholder="Search stocks..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            />
            <span className="absolute inset-y-0 left-3 flex items-center text-gray-400">
            <SearchIcon className="w-4 h-4" />
            </span>
        </div>

        {/* Scan‑type dropdown */}
        <select
            className="w-full p-2 border border-gray-300 rounded-md bg-white"
            value={scanType}
            onChange={(e) => setScanType(e.target.value)}
        >
            <option value="all">All Scanners</option>
            <option value="44ma">44MA</option>
            <option value="fib">Fib</option>
            <option value="rsi">RSI</option>
        </select>

        {/* Stock list */}
        <div className="h-96 overflow-y-auto rounded-xl shadow-inner bg-white border border-gray-200">
            {/* sticky header */}
            <div className="sticky top-0 z-10 flex bg-white/90 backdrop-blur px-4 py-2 font-medium text-sm border-b">
            <span className="w-10" />
            <span className="flex-1">Symbol</span>
            <span className="w-20 text-center">Info</span>
            </div>

            <ul className="divide-y divide-gray-200 text-sm">
            {filteredStocks.map((stock) => (
                <li key={stock} className="flex items-center px-4 py-2 hover:bg-gray-50">
                {/* checkbox + symbol */}
                <label className="flex items-center gap-3 cursor-pointer flex-1">
                    <input
                    type="checkbox"
                    checked={selected.includes(stock)}
                    onChange={() => toggleSelection(stock)}
                    className="h-5 w-5 rounded border-gray-300 text-[#a83232] focus:ring-[#a83232]"
                    />
                    <span className="font-medium text-slate-700">{stock}</span>
                </label>

                {/* status badge + magnifier */}
                <div className="flex items-center gap-3 w-20 justify-end">
                    {statusBadge(scanStatus[stock])}
                    <button
                    onClick={() => viewSummary(stock)}
                    className="p-1 rounded hover:bg-gray-100"
                    title="View last summary"
                    >
                    <SearchIcon className="w-4 h-4 text-gray-500 hover:text-[#a83232]" />
                    </button>
                </div>
                </li>
            ))}
            </ul>
        </div>

        {/* Run button */}
        <button
            className={`w-full py-2 font-medium text-white rounded-md transition hover:shadow-lg ${
            !selected.length || isScanning
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-[#a83232] hover:bg-red-700"
            }`}
            onClick={runScannersOnSelected}
            disabled={!selected.length || isScanning}
        >
            {isScanning ? "Scanning…" : "Run Scan on Selected"}
        </button>
        </div>

        {/* ── Scan results modal ── */}
        {showModal && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
            <div className="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-md">
            <h2 className="text-xl font-semibold mb-4">Scan Summary</h2>
            <ul className="space-y-4 text-sm max-h-64 overflow-y-auto">
                {scanResults.map((entry) => (
                <li key={entry.symbol}>
                    <div className="font-semibold mb-1">{entry.symbol}</div>
                    <ul className="pl-4">
                    {entry.result.error ? (
                        <li className="text-red-600">Scan failed</li>
                    ) : (
                        ["44MA", "FIB", "RSI"].map((t) => (
                        <li key={t} className="flex justify-between">
                            <span>{t}</span>
                            <span
                            className={
                                entry.result[t.toLowerCase()]
                                ? "text-green-600"
                                : "text-gray-400"
                            }
                            >
                            {entry.result[t.toLowerCase()] ? "✔️ Yes" : "— No"}
                            </span>
                        </li>
                        ))
                    )}
                    </ul>
                </li>
                ))}
            </ul>
            <button
                className="mt-6 w-full bg-[#a83232] text-white py-2 rounded-md"
                onClick={() => setShowModal(false)}
            >
                Close
            </button>
            </div>
        </div>
        )}

        {/* ── Saved summary modal ── */}
        {showSummary && summaryData && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
            <div className="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-md">
            <h2 className="text-xl font-semibold mb-4">
                Saved Summary – {summaryData.symbol}
            </h2>

            <ul className="space-y-3 text-sm">
                {["44ma", "fib", "rsi"].map((t) => (
                <li key={t} className="flex justify-between">
                    <span className="uppercase">{t}</span>
                    <span
                    className={
                        summaryData.summary[t] ? "text-green-600" : "text-gray-400"
                    }
                    >
                    {summaryData.summary[t] ? "✔️ Yes" : "— No"}
                    </span>
                </li>
                ))}
            </ul>

            <button
                className="mt-6 w-full bg-[#a83232] text-white py-2 rounded-md"
                onClick={() => setShowSummary(false)}
            >
                Close
            </button>
            </div>
        </div>
        )}
    </div>
    );


};

export default StockScannerPanel;