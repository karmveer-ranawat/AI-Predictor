// --- src/components/StockCard.jsx ---
const StockCard = ({ symbol, onRunScanner }) => {
  return (
    <div className="flex items-center justify-between p-4 mb-2 bg-white rounded shadow">
      <span className="font-medium">{symbol}</span>
      <div className="space-x-2">
        <button
          className="bg-gray-200 px-3 py-1 rounded hover:bg-gray-300"
          onClick={() => onRunScanner("ma44")}
        >
          44MA
        </button>
        <button
          className="bg-gray-200 px-3 py-1 rounded hover:bg-gray-300"
          onClick={() => onRunScanner("fib")}
        >
          FIB
        </button>
        <button
          className="bg-gray-200 px-3 py-1 rounded hover:bg-gray-300"
          onClick={() => onRunScanner("rsi")}
        >
          RSI
        </button>
      </div>
    </div>
  );
};

export default StockCard;
