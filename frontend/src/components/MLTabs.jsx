// src/components/MLTabs.jsx
import { useState, useEffect } from "react";
import axios from "../api/axios";

const tabs = ["Collect", "Preprocess", "Merge", "Train", "Predict", "Models"];

const MLTabs = () => {
  const [active, setActive] = useState("Collect");

  /* common-ish state */
  const [symbol, setSymbol] = useState("");
  const [years, setYears] = useState(4);
  const [interval, setInterval] = useState("day");

  const [log, setLog] = useState("");               // shows result json
  const [symbolsList, setSymbolsList] = useState([]); // for dropdowns
  const [models, setModels] = useState([]);           // model list

  /* fetch symbols once for dropdowns */
  useEffect(() => {
    (async () => {
      try {
        const res = await axios.get("/scanner/all_symbols");
        setSymbolsList(res.data.symbols);
      } catch (e) {
        console.error(e);
      }
    })();
  }, []);

  /* helper to prettify backend response */
  const showResp = (obj) => setLog(JSON.stringify(obj, null, 2));

  // ───────────────────────────────── Collect
  const fetchSingle = async () => {
    try {
      const res = await axios.get("/ml/fetch_single", {
        params: { symbol, years, interval },
      });
      showResp(res.data);
    } catch (e) {
      showResp(e.response?.data || e.message);
    }
  };

  const fetchBatch = async () => {
    try {
      const res = await axios.get("/ml/fetch_batch", {
        params: { years, interval },
      });
      showResp(res.data);
    } catch (e) {
      showResp(e.response?.data || e.message);
    }
  };

  // ──────────────────────────────── Preprocess
  const preprocessSingle = async () => {
    try {
      const res = await axios.get("/ml/preprocess_stock", {
        params: { symbol },
      });
      showResp(res.data);
    } catch (e) {
      showResp(e.response?.data || e.message);
    }
  };
  const preprocessAll = async () => {
    try {
      const res = await axios.get("/ml/preprocess_all");
      showResp(res.data);
    } catch (e) {
      showResp(e.response?.data || e.message);
    }
  };

  // ──────────────────────────────── Merge
  const mergeEncode = async () => {
    try {
      const res = await axios.get("/ml/merge_encode");
      showResp(res.data);
    } catch (e) {
      showResp(e.response?.data || e.message);
    }
  };

  // ──────────────────────────────── Train
  const [epochs, setEpochs] = useState(30);
  const [batchSize, setBatchSize] = useState(32);
  const [testRatio, setTestRatio] = useState(0.2);

  const trainGlobal = async () => {
    try {
      const res = await axios.get("/ml/train_multi", {
        params: { epochs, batch_size: batchSize, test_ratio: testRatio },
      });
      showResp(res.data);
      await loadModels(); // refresh list
    } catch (e) {
      showResp(e.response?.data || e.message);
    }
  };
  const trainSingle = async () => {
    try {
      const res = await axios.get("/ml/train_single", {
        params: { symbol, epochs, batch_size: batchSize, test_ratio: testRatio },
      });
      showResp(res.data);
      await loadModels();
    } catch (e) {
      showResp(e.response?.data || e.message);
    }
  };

  // ──────────────────────────────── Models list
  const loadModels = async () => {
    try {
      const res = await axios.get("/ml/models");
      setModels(res.data.models);
    } catch (e) {
      console.error(e);
    }
  };
  useEffect(() => {
    loadModels();
  }, []);
//   useEffect(loadModels, []);

  // ──────────────────────────────── Predict
  const [selModel, setSelModel] = useState("global");
  const [predRows, setPredRows] = useState(30);

  const predictSymbol = async () => {
    try {
      const res = await axios.post("/ml/ml/predict", null, {
        params: { symbol, model_name: selModel, top_n_rows: predRows },
      });
      showResp(res.data);
    } catch (e) {
      showResp(e.response?.data || e.message);
    }
  };

  const predictCSV = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const form = new FormData();
    form.append("file", file);
    try {
      const res = await axios.post("/ml/ml/predict", form, {
        params: { model_name: selModel, top_n_rows: predRows },
        headers: { "Content-Type": "multipart/form-data" },
      });
      showResp(res.data);
    } catch (e) {
      showResp(e.response?.data || e.message);
    }
  };

  // ──────────────────────────────── UI helpers
  const Input = ({ label, ...rest }) => (
    <label className="block text-sm mb-2">
      {label}
      <input {...rest} className="mt-1 w-full border rounded px-2 py-1" />
    </label>
  );

  const Section = ({ children }) => (
    <div className="space-y-4 bg-white border p-5 rounded shadow">{children}</div>
  );

  // ──────────────────────────────── Tab panels
  const renderPanel = () => {
    switch (active) {
      /* -------- Collect -------- */
      case "Collect":
        return (
          <Section>
            <Input
              label="Symbol"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            />
            <Input
              label="Years of data"
              type="number"
              value={years}
              min={1}
              onChange={(e) => setYears(e.target.value)}
            />
            <Input
              label="Interval"
              value={interval}
              onChange={(e) => setInterval(e.target.value)}
            />
            <div className="flex gap-4">
              <button className="btn-primary" onClick={fetchSingle}>
                Fetch Single
              </button>
              <button className="btn-secondary" onClick={fetchBatch}>
                Fetch Batch
              </button>
            </div>
          </Section>
        );

      /* -------- Preprocess -------- */
      case "Preprocess":
        return (
          <Section>
            <Input
              label="Symbol for single preprocess"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            />
            <div className="flex gap-4">
              <button className="btn-primary" onClick={preprocessSingle}>
                Preprocess Single
              </button>
              <button className="btn-secondary" onClick={preprocessAll}>
                Preprocess All
              </button>
            </div>
          </Section>
        );

      /* -------- Merge -------- */
      case "Merge":
        return (
          <Section>
            <button className="btn-primary w-full" onClick={mergeEncode}>
              Merge &amp; Encode Datasets
            </button>
          </Section>
        );

      /* -------- Train -------- */
      case "Train":
        return (
          <Section>
            <div className="grid grid-cols-2 gap-4">
              <Input
                label="Epochs"
                type="number"
                value={epochs}
                onChange={(e) => setEpochs(e.target.value)}
              />
              <Input
                label="Batch size"
                type="number"
                value={batchSize}
                onChange={(e) => setBatchSize(e.target.value)}
              />
              <Input
                label="Test ratio"
                type="number"
                step="0.05"
                value={testRatio}
                onChange={(e) => setTestRatio(e.target.value)}
              />
            </div>

            <hr className="my-2" />

            <Input
              label="Symbol for single‑stock training"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            />

            <div className="flex gap-4">
              <button className="btn-primary flex-1" onClick={trainGlobal}>
                Train Global
              </button>
              <button className="btn-secondary flex-1" onClick={trainSingle}>
                Train Single
              </button>
            </div>
          </Section>
        );

      /* -------- Predict -------- */
      case "Predict":
        return (
          <Section>
            <label className="block text-sm mb-2">
              Select model
              <select
                value={selModel}
                onChange={(e) => setSelModel(e.target.value)}
                className="mt-1 w-full border rounded px-2 py-1 bg-white"
              >
                <option value="global">global</option>
                {models.map((m) => (
                  <option key={m.name} value={m.name}>
                    {m.name}
                  </option>
                ))}
              </select>
            </label>

            <Input
              label="Symbol to predict"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            />

            <Input
              label="Top N rows"
              type="number"
              value={predRows}
              onChange={(e) => setPredRows(e.target.value)}
            />

            <div className="flex gap-4">
              <button className="btn-primary flex-1" onClick={predictSymbol}>
                Predict (symbol)
              </button>
              <label className="btn-secondary flex-1 text-center cursor-pointer">
                Upload CSV
                <input type="file" accept=".csv" hidden onChange={predictCSV} />
              </label>
            </div>
          </Section>
        );

      /* -------- Models list -------- */
      case "Models":
        return (
          <Section>
            <button
              className="btn-secondary mb-4"
              onClick={loadModels}
            >
              Refresh list
            </button>
            <div className="max-h-64 overflow-y-auto border rounded">
              <table className="w-full text-sm">
                <thead className="bg-gray-100 sticky top-0">
                  <tr>
                    <th className="px-2 py-1 text-left">Name</th>
                    <th className="px-2 py-1">Acc</th>
                    <th className="px-2 py-1">Epochs</th>
                  </tr>
                </thead>
                <tbody>
                  {models.map((m) => (
                    <tr key={m.name} className="odd:bg-white even:bg-gray-50">
                      <td className="px-2 py-1">{m.name}</td>
                      <td className="px-2 py-1 text-center">
                        {(m.accuracy * 100).toFixed(1)}%
                      </td>
                      <td className="px-2 py-1 text-center">{m.epochs}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Section>
        );

      default:
        return null;
    }
  };

  return (
    <div className="w-full">
      {/* Tab bar */}
      <div className="flex gap-4 mb-4 border-b">
        {tabs.map((t) => (
          <button
            key={t}
            onClick={() => setActive(t)}
            className={`pb-2 font-medium ${
              active === t
                ? "border-b-2 border-[#a83232] text-[#a83232]"
                : "text-gray-500 hover:text-[#a83232]"
            }`}
          >
            {t}
          </button>
        ))}
      </div>

      {/* Panel */}
      {renderPanel()}

      {/* Simple log box */}
      {log && (
        <pre className="mt-4 bg-gray-900 text-gray-100 text-xs p-4 rounded max-h-64 overflow-y-auto">
          {log}
        </pre>
      )}
    </div>
  );
};

/* small utility button classes (Tailwind) */
const Btn = "px-4 py-2 rounded text-white";
export const btnPrimary = `${Btn} bg-[#a83232] hover:bg-red-700`;
export const btnSecondary = `${Btn} bg-gray-500 hover:bg-gray-600`;
export default MLTabs;
