import React, { useState } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";

const BreastCancer = () => {
  // Backend-required keys (DO NOT CHANGE) - All 30 features in correct order
  const [inputs, setInputs] = useState({
    "mean radius": "",
    "mean texture": "",
    "mean perimeter": "",
    "mean area": "",
    "mean smoothness": "",
    "mean compactness": "",
    "mean concavity": "",
    "mean concave points": "",
    "mean symmetry": "",
    "mean fractal dimension": "",
    "radius error": "",
    "texture error": "",
    "perimeter error": "",
    "area error": "",
    "smoothness error": "",
    "compactness error": "",
    "concavity error": "",
    "concave points error": "",
    "symmetry error": "",
    "fractal dimension error": "",
    "worst radius": "",
    "worst texture": "",
    "worst perimeter": "",
    "worst area": "",
    "worst smoothness": "",
    "worst compactness": "",
    "worst concavity": "",
    "worst concave points": "",
    "worst symmetry": "",
    "worst fractal dimension": "",
  });

  const [result, setResult] = useState(null);
  const [probability, setProbability] = useState(null);
  const [featureImportance, setFeatureImportance] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // 🔹 Fields info shown to user - User-friendly labels and ranges for all 30 features
  const fields = {
    "mean radius": { label: "Mean Radius", range: "6.0 – 28.0 mm", unit: "mm" },
    "mean texture": { label: "Mean Texture", range: "9.0 – 40.0", unit: "standard deviations" },
    "mean perimeter": { label: "Mean Perimeter", range: "40.0 – 190.0 mm", unit: "mm" },
    "mean area": { label: "Mean Area", range: "140.0 – 2500.0 mm²", unit: "mm²" },
    "mean smoothness": { label: "Mean Smoothness", range: "0.05 – 0.16", unit: "local variation" },
    "mean compactness": { label: "Mean Compactness", range: "0.02 – 0.35", unit: "perimeter²/area - 1" },
    "mean concavity": { label: "Mean Concavity", range: "0.0 – 0.43", unit: "severity of concave portions" },
    "mean concave points": { label: "Mean Concave Points", range: "0.0 – 0.20", unit: "number of concave portions" },
    "mean symmetry": { label: "Mean Symmetry", range: "0.1 – 0.27", unit: "symmetry measure" },
    "mean fractal dimension": { label: "Mean Fractal Dimension", range: "0.05 – 0.10", unit: "coastline approximation" },
    "radius error": { label: "Radius Error", range: "0.1 – 2.0 mm", unit: "mm" },
    "texture error": { label: "Texture Error", range: "0.2 – 4.0", unit: "standard deviations" },
    "perimeter error": { label: "Perimeter Error", range: "0.5 – 20.0 mm", unit: "mm" },
    "area error": { label: "Area Error", range: "2.0 – 550.0 mm²", unit: "mm²" },
    "smoothness error": { label: "Smoothness Error", range: "0.001 – 0.03", unit: "local variation" },
    "compactness error": { label: "Compactness Error", range: "0.002 – 0.08", unit: "perimeter²/area - 1" },
    "concavity error": { label: "Concavity Error", range: "0.0 – 0.1", unit: "severity of concave portions" },
    "concave points error": { label: "Concave Points Error", range: "0.0 – 0.05", unit: "number of concave portions" },
    "symmetry error": { label: "Symmetry Error", range: "0.008 – 0.08", unit: "symmetry measure" },
    "fractal dimension error": { label: "Fractal Dimension Error", range: "0.001 – 0.03", unit: "coastline approximation" },
    "worst radius": { label: "Worst Radius", range: "7.0 – 36.0 mm", unit: "mm" },
    "worst texture": { label: "Worst Texture", range: "12.0 – 50.0", unit: "standard deviations" },
    "worst perimeter": { label: "Worst Perimeter", range: "50.0 – 250.0 mm", unit: "mm" },
    "worst area": { label: "Worst Area", range: "200.0 – 4300.0 mm²", unit: "mm²" },
    "worst smoothness": { label: "Worst Smoothness", range: "0.07 – 0.22", unit: "local variation" },
    "worst compactness": { label: "Worst Compactness", range: "0.05 – 0.85", unit: "perimeter²/area - 1" },
    "worst concavity": { label: "Worst Concavity", range: "0.0 – 1.0", unit: "severity of concave portions" },
    "worst concave points": { label: "Worst Concave Points", range: "0.0 – 0.30", unit: "number of concave portions" },
    "worst symmetry": { label: "Worst Symmetry", range: "0.15 – 0.45", unit: "symmetry measure" },
    "worst fractal dimension": { label: "Worst Fractal Dimension", range: "0.06 – 0.15", unit: "coastline approximation" },
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setInputs((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    setProbability(null);
    setFeatureImportance([]);

    try {
      const response = await fetch("/api/breastcancer/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(inputs),
      });

      if (!response.ok) {
        throw new Error(`Server Error: ${response.status}`);
      }

      const data = await response.json();

      setResult(data.prediction_label);
      setProbability(data.confidence.toFixed(2));
      setFeatureImportance(data.feature_importance || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Prepare data for the bar chart
  const chartData = featureImportance.map((item) => ({
    name: item.label,
    importance: (item.importance * 100).toFixed(2),
    fullName: item.feature,
  }));

  return (
    <div className="min-h-screen bg-linear-to-r from-black via-gray-900 to-black flex items-center justify-center p-4">
      <div className="bg-gray-800 bg-opacity-90 rounded-lg shadow-2xl p-8 w-full max-w-6xl">
        
        <h1 className="text-4xl font-bold text-pink-500 text-center mb-6">
          Breast Cancer Classification
        </h1>
        
        <p className="text-gray-400 text-center mb-6">
          Enter the 30 cell nucleus features to predict if the tumor is Benign or Malignant
        </p>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Mean Features - Row 1 */}
          <div className="mb-4">
            <h3 className="text-lg font-semibold text-pink-400 mb-3 border-b border-pink-400 pb-1">
              Mean Features (1-10)
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
              {Object.keys(fields)
                .filter((key) => key.startsWith("mean ") && !key.includes("error"))
                .slice(0, 5)
                .map((key) => (
                  <div key={key} className="flex flex-col">
                    <label className="text-white font-semibold mb-1 text-sm">
                      {fields[key].label}
                    </label>
                    <span className="text-gray-400 text-xs mb-1">
                      Range: {fields[key].range}
                    </span>
                    <input
                      type="number"
                      name={key}
                      value={inputs[key]}
                      onChange={handleInputChange}
                      step="any"
                      required
                      placeholder="0.00"
                      className="bg-gray-700 text-white border border-gray-600 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-pink-500"
                    />
                  </div>
                ))}
            </div>
          </div>

          {/* Mean Features - Row 2 */}
          <div className="mb-4">
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
              {Object.keys(fields)
                .filter((key) => key.startsWith("mean ") && !key.includes("error"))
                .slice(5, 10)
                .map((key) => (
                  <div key={key} className="flex flex-col">
                    <label className="text-white font-semibold mb-1 text-sm">
                      {fields[key].label}
                    </label>
                    <span className="text-gray-400 text-xs mb-1">
                      Range: {fields[key].range}
                    </span>
                    <input
                      type="number"
                      name={key}
                      value={inputs[key]}
                      onChange={handleInputChange}
                      step="any"
                      required
                      placeholder="0.00"
                      className="bg-gray-700 text-white border border-gray-600 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-pink-500"
                    />
                  </div>
                ))}
            </div>
          </div>

          {/* Error Features - Row 3 */}
          <div className="mb-4">
            <h3 className="text-lg font-semibold text-pink-400 mb-3 border-b border-pink-400 pb-1">
              Error Features (11-20)
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
              {Object.keys(fields)
                .filter((key) => key.includes("error"))
                .slice(0, 5)
                .map((key) => (
                  <div key={key} className="flex flex-col">
                    <label className="text-white font-semibold mb-1 text-sm">
                      {fields[key].label}
                    </label>
                    <span className="text-gray-400 text-xs mb-1">
                      Range: {fields[key].range}
                    </span>
                    <input
                      type="number"
                      name={key}
                      value={inputs[key]}
                      onChange={handleInputChange}
                      step="any"
                      required
                      placeholder="0.00"
                      className="bg-gray-700 text-white border border-gray-600 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-pink-500"
                    />
                  </div>
                ))}
            </div>
          </div>

          {/* Error Features - Row 4 */}
          <div className="mb-4">
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
              {Object.keys(fields)
                .filter((key) => key.includes("error"))
                .slice(5, 10)
                .map((key) => (
                  <div key={key} className="flex flex-col">
                    <label className="text-white font-semibold mb-1 text-sm">
                      {fields[key].label}
                    </label>
                    <span className="text-gray-400 text-xs mb-1">
                      Range: {fields[key].range}
                    </span>
                    <input
                      type="number"
                      name={key}
                      value={inputs[key]}
                      onChange={handleInputChange}
                      step="any"
                      required
                      placeholder="0.00"
                      className="bg-gray-700 text-white border border-gray-600 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-pink-500"
                    />
                  </div>
                ))}
            </div>
          </div>

          {/* Worst Features - Row 5 */}
          <div className="mb-4">
            <h3 className="text-lg font-semibold text-pink-400 mb-3 border-b border-pink-400 pb-1">
              Worst Features (21-30)
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
              {Object.keys(fields)
                .filter((key) => key.startsWith("worst ") && !key.includes("error"))
                .slice(0, 5)
                .map((key) => (
                  <div key={key} className="flex flex-col">
                    <label className="text-white font-semibold mb-1 text-sm">
                      {fields[key].label}
                    </label>
                    <span className="text-gray-400 text-xs mb-1">
                      Range: {fields[key].range}
                    </span>
                    <input
                      type="number"
                      name={key}
                      value={inputs[key]}
                      onChange={handleInputChange}
                      step="any"
                      required
                      placeholder="0.00"
                      className="bg-gray-700 text-white border border-gray-600 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-pink-500"
                    />
                  </div>
                ))}
            </div>
          </div>

          {/* Worst Features - Row 6 */}
          <div className="mb-4">
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
              {Object.keys(fields)
                .filter((key) => key.startsWith("worst ") && !key.includes("error"))
                .slice(5, 10)
                .map((key) => (
                  <div key={key} className="flex flex-col">
                    <label className="text-white font-semibold mb-1 text-sm">
                      {fields[key].label}
                    </label>
                    <span className="text-gray-400 text-xs mb-1">
                      Range: {fields[key].range}
                    </span>
                    <input
                      type="number"
                      name={key}
                      value={inputs[key]}
                      onChange={handleInputChange}
                      step="any"
                      required
                      placeholder="0.00"
                      className="bg-gray-700 text-white border border-gray-600 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-pink-500"
                    />
                  </div>
                ))}
            </div>
          </div>

          <div className="flex justify-center">
            <button
              type="submit"
              disabled={loading}
              className="bg-pink-600 hover:bg-pink-700 disabled:bg-pink-800 text-white font-bold py-3 px-8 rounded-lg transition"
            >
              {loading ? "Analyzing..." : "Predict Diagnosis"}
            </button>
          </div>
        </form>

        {loading && (
          <p className="text-pink-400 text-center mt-6">
            Analyzing tumor characteristics...
          </p>
        )}

        {error && (
          <p className="text-red-400 text-center mt-6">
            Error: {error}
          </p>
        )}

        {result && !loading && (
          <div className="mt-6 space-y-6">
            {/* Prediction Result */}
            <div className="p-4 bg-gray-700 rounded-lg text-center">
              <h2 className="text-white text-xl font-semibold mb-2">
                Prediction Result
              </h2>
              <p className={`text-2xl font-bold ${result === "Benign" ? "text-green-400" : "text-red-400"}`}>
                {result}
              </p>
              <p className="text-gray-300 mt-2">
                Confidence: <strong>{probability}%</strong>
              </p>
            </div>

            {/* Feature Importance Chart */}
            {featureImportance.length > 0 && (
              <div className="p-4 bg-gray-700 rounded-lg">
                <h3 className="text-white text-lg font-semibold mb-4 text-center">
                  Top 10 Feature Importance
                </h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#4a5568" />
                      <XAxis type="number" domain={[0, 'auto']} tick={{ fill: '#a0aec0' }} />
                      <YAxis 
                        type="category" 
                        dataKey="name" 
                        width={150} 
                        tick={{ fill: '#e2e8f0', fontSize: 11 }}
                      />
                      <Tooltip 
                        contentStyle={{ backgroundColor: '#2d3748', border: '1px solid #4a5568', borderRadius: '8px' }}
                        labelStyle={{ color: '#e2e8f0' }}
                        formatter={(value, name, props) => [`${value}%`, 'Importance']}
                      />
                      <Bar dataKey="importance" radius={[0, 4, 4, 0]}>
                        {chartData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={index < 3 ? '#ec4899' : '#be185d'} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default BreastCancer;

