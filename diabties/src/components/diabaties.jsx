import React, { useState } from 'react';

const Diabaties = () => {

  // Backend-required keys (DO NOT CHANGE)
  const [inputs, setInputs] = useState({
    age: '',
    bmi: '',
    bp: '',
    s1: '',
    s2: '',
    s3: '',
    s4: '',
    s5: '',
    s6: ''
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // 🔹 Field labels shown to user
  const fields = {
    age: { label: "Age (years)", range: "20 – 80" },
    bmi: { label: "BMI", range: "15 – 70" },
    bp: { label: "Blood Pressure", range: "70 – 220" },
    s1: { label: "Cholesterol (mg/dL)", range: "140 – 300" },
    s2: { label: "LDL Cholesterol", range: "80 – 200" },
    s3: { label: "HDL Cholesterol", range: "20 – 80" },
    s4: { label: "Cholesterol Ratio", range: "2 – 7" },
    s5: { label: "Triglycerides", range: "4 – 9" },
    s6: { label: "Glucose Level", range: "80 – 250" }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setInputs(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(inputs), // 👈 s1 s2 s3 sent correctly
      });

      if (!response.ok) {
        throw new Error(`Server Error: ${response.status}`);
      }

      const data = await response.json();
      setPrediction(data.prediction.toFixed(2));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-r from-black via-gray-900 to-black flex items-center justify-center p-4">
      <div className="bg-gray-800 bg-opacity-90 rounded-lg shadow-2xl p-8 w-full max-w-4xl">
        
        <h1 className="text-4xl font-bold text-amber-500 text-center mb-6">
          Diabetes Prediction Model
        </h1>

        <form onSubmit={handleSubmit} className="space-y-6">

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
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
              Predict Diabetes
            </button>
          </div>
        </form>

        {loading && (
          <p className="text-yellow-400 text-center mt-6">
            Predicting...
          </p>
        )}

        {error && (
          <p className="text-red-400 text-center mt-6">
            Error: {error}
          </p>
        )}

        {prediction && !loading && (
          <div className="mt-6 p-4 bg-gray-700 rounded-lg text-center">
            <h2 className="text-white text-xl font-semibold mb-2">
              Prediction Result
            </h2>
            <p className="text-green-400 text-lg">
              Predicted Diabetes Value: <strong>{prediction}</strong>
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Diabaties;
