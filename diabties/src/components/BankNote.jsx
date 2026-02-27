import React, { useState } from "react";

const BankNote = () => {

  // Backend-required keys (DO NOT CHANGE)
  const [inputs, setInputs] = useState({
    var: "",
    skew: "",
    curt: "",
    entr: ""
  });

  const [result, setResult] = useState(null);
  const [probability, setProbability] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // 🔹 Fields info shown to user
  const fields = {
    var: { label: "Surface Texture Quality", range: "-10 to 10" },
    skew: { label: "Pattern Alignment", range: "-10 to 10" },
    curt: { label: "Print Quality", range: "-10 to 10" },
    entr: { label: "Image Detail Complexity", range: "-10 to 10" }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setInputs(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    setProbability(null);

    try {
     const response = await fetch("/api/banknote/authenticate", {
     method: "POST",
     headers: { "Content-Type": "application/json" },
     body: JSON.stringify(inputs),
});

      if (!response.ok) {
        throw new Error(`Server Error: ${response.status}`);
      }

      const data = await response.json();

      setResult(data.prediction === 1 ? "Authentic Note" : "Fake Note");
      setProbability((data.probability[0][data.prediction] * 100).toFixed(2));

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-r from-black via-gray-900 to-black flex items-center justify-center p-4">
      <div className="bg-gray-800 bg-opacity-90 rounded-lg shadow-2xl p-8 w-full max-w-3xl">

        <h1 className="text-4xl font-bold text-amber-500 text-center mb-6">
          Bank Note Authentication
        </h1>

        <form onSubmit={handleSubmit} className="space-y-6">

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {Object.keys(inputs).map((key) => (
              <div key={key} className="flex flex-col">

                <label className="text-white font-semibold mb-1">
                  {fields[key].label}
                </label>

                <span className="text-gray-400 text-sm mb-2">
                  Range: {fields[key].range}
                </span>

                <input
                  type="number"
                  name={key}
                  value={inputs[key]}
                  onChange={handleInputChange}
                  step="any"
                  required
                  placeholder={`Enter ${fields[key].label}`}
                  className="bg-gray-700 text-white border border-gray-600 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-yellow-500"
                />
              </div>
            ))}
          </div>

          <div className="flex justify-center">
            <button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg transition"
            >
              Authenticate Note
            </button>
          </div>
        </form>

        {loading && (
          <p className="text-yellow-400 text-center mt-6">
            Authenticating...
          </p>
        )}

        {error && (
          <p className="text-red-400 text-center mt-6">
            Error: {error}
          </p>
        )}

        {result && !loading && (
          <div className="mt-6 p-4 bg-gray-700 rounded-lg text-center">
            <h2 className="text-white text-xl font-semibold mb-2">
              Result
            </h2>
            <p className={`text-lg font-bold ${result === "Authentic Note" ? "text-green-400" : "text-red-400"}`}>
              {result}
            </p>
            <p className="text-gray-300 mt-2">
              Confidence: <strong>{probability}%</strong>
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default BankNote;
