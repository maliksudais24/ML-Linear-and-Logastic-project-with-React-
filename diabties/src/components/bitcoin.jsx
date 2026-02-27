import React, { useState } from "react";

const Bitcoin = () => {
  // Backend-required keys (DO NOT CHANGE)
  const [inputs, setInputs] = useState({
    price: ""
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setInputs(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch("/api/bitcoin/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(inputs),
      });

      if (!response.ok) {
        throw new Error(`Server Error: ${response.status}`);
      }

      const data = await response.json();

      setResult({
        currentPrice: data.current_price,
        predictedPrice: data.predicted_price,
        priceChange: data.price_change,
        priceChangePercent: data.price_change_percent,
        timeframe: data.prediction_timeframe
      });

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-orange-900 via-yellow-900 to-orange-900 flex items-center justify-center p-4">
      <div className="bg-gray-800 bg-opacity-90 rounded-lg shadow-2xl p-8 w-full max-w-2xl">
        
        <div className="text-center mb-6">
          <h1 className="text-4xl font-bold text-orange-500 mb-2">
            Bitcoin Price Prediction
          </h1>
          <p className="text-gray-400">
            Predict Bitcoin price for the next 2 minutes
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="flex flex-col">
            <label className="text-white font-semibold mb-2">
              Current Bitcoin Price (USD)
            </label>
            <span className="text-gray-400 text-sm mb-2">
              Enter the current BTC/USD price
            </span>
            <input
              type="number"
              name="price"
              value={inputs.price}
              onChange={handleInputChange}
              step="0.01"
              required
              placeholder="e.g., 45000.00"
              className="bg-gray-700 text-white border border-gray-600 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-orange-500 text-lg"
            />
          </div>

          <div className="flex justify-center">
            <button
              type="submit"
              disabled={loading}
              className="bg-orange-600 hover:bg-orange-700 disabled:bg-gray-600 text-white font-bold py-3 px-8 rounded-lg transition"
            >
              {loading ? "Predicting..." : "Predict Price"}
            </button>
          </div>
        </form>

        {loading && (
          <p className="text-orange-400 text-center mt-6">
            Analyzing price patterns...
          </p>
        )}

        {error && (
          <p className="text-red-400 text-center mt-6">
            Error: {error}
          </p>
        )}

        {result && !loading && (
          <div className="mt-6 p-6 bg-gray-700 rounded-lg">
            <h2 className="text-white text-xl font-semibold mb-4 text-center">
              Prediction Result
            </h2>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-600 p-4 rounded-lg">
                <p className="text-gray-400 text-sm">Current Price</p>
                <p className="text-white text-xl font-bold">
                  ${result.currentPrice.toLocaleString()}
                </p>
              </div>
              
              <div className="bg-gray-600 p-4 rounded-lg">
                <p className="text-gray-400 text-sm">Predicted Price (2 min)</p>
                <p className="text-green-400 text-xl font-bold">
                  ${result.predictedPrice.toLocaleString()}
                </p>
              </div>
              
              <div className="bg-gray-600 p-4 rounded-lg col-span-2">
                <p className="text-gray-400 text-sm">Expected Change</p>
                <p className={`text-2xl font-bold ${result.priceChange >= 0 ? "text-green-400" : "text-red-400"}`}>
                  {result.priceChange >= 0 ? "+" : ""}{result.priceChange.toLocaleString()} 
                  ({result.priceChangePercent >= 0 ? "+" : ""}{result.priceChangePercent}%)
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Bitcoin;

