import { useState } from 'react';
import { motion }   from 'framer-motion';
import AQIGauge       from '../components/AQIGauge';
import HealthAdvisory from '../components/HealthAdvisory';
import { CITIES, POLLUTANTS, getAQIBucket } from '../utils/aqiHelpers';
import api from '../utils/api';

const defaultInputs = {
  PM2_5: 60, PM10: 100, NO2: 40, CO: 1.5, SO2: 20, O3: 50
};

export default function Predict() {
  const [city,    setCity]    = useState('Delhi');
  const [inputs,  setInputs]  = useState(defaultInputs);
  const [result,  setResult]  = useState(null);
  const [bucket,  setBucket]  = useState(null);
  const [loading, setLoading] = useState(false);
  const [error,   setError]   = useState(null);

  const handleSlider = (key, value) =>
    setInputs(prev => ({ ...prev, [key]: Number(value) }));

  const handlePredict = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.post('/predict', {
        city    : city,
        month   : new Date().getMonth() + 1,
        'PM2.5' : inputs.PM2_5,
        PM10    : inputs.PM10,
        NO      : 0,
        NO2     : inputs.NO2,
        NOx     : 0,
        NH3     : 0,
        CO      : inputs.CO,
        SO2     : inputs.SO2,
        O3      : inputs.O3,
        Benzene : 0,
        Toluene : 0,
        Xylene  : 0,
      });
      setResult(res.data.aqi_predicted);
      setBucket(res.data.aqi_bucket);
    } catch (err) {
      setError('Prediction failed. Backend may be waking up — try again in 30s.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-6 pt-28 pb-16">

      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-10"
      >
        <h1 className="text-4xl font-bold text-white">
          Predict <span className="text-blue-400">AQI</span>
        </h1>
        <p className="text-slate-400 mt-2">
          Enter pollutant readings to get a real-time AQI prediction
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

        {/* Input Panel */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-slate-800 rounded-2xl p-6 border border-slate-700"
        >
          {/* City Selector */}
          <div className="mb-6">
            <label className="text-slate-400 text-sm mb-2 block">City</label>
            <select
              value={city}
              onChange={e => setCity(e.target.value)}
              className="w-full bg-slate-700 text-white rounded-xl px-4 py-2.5
                         border border-slate-600 focus:outline-none
                         focus:border-blue-500 text-sm"
            >
              {CITIES.map(c => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>

          {/* Pollutant Sliders */}
          {POLLUTANTS.map(p => (
            <div key={p.key} className="mb-5">
              <div className="flex justify-between mb-1">
                <label className="text-slate-300 text-sm">{p.label}</label>
                <span className="text-blue-400 text-sm font-medium">
                  {inputs[p.key.replace('.', '_')]} {p.unit}
                </span>
              </div>
              <input
                type="range"
                min={p.min}
                max={p.max}
                step={p.key === 'CO' ? 0.1 : 1}
                value={inputs[p.key.replace('.', '_')]}
                onChange={e =>
                  handleSlider(p.key.replace('.', '_'), e.target.value)}
                className="w-full accent-blue-400"
              />
              <div className="flex justify-between text-slate-600 text-xs mt-0.5">
                <span>{p.min}</span>
                <span>{p.max}</span>
              </div>
            </div>
          ))}

          <button
            onClick={handlePredict}
            disabled={loading}
            className="w-full mt-4 py-3 rounded-xl font-semibold text-white
                       bg-blue-600 hover:bg-blue-500 disabled:opacity-50
                       transition-colors duration-200"
          >
            {loading ? 'Predicting...' : 'Predict AQI →'}
          </button>

          {/* Error message */}
          {error && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mt-3 text-red-400 text-xs text-center"
            >
              {error}
            </motion.p>
          )}
        </motion.div>

        {/* Result Panel */}
        <motion.div
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex flex-col gap-6"
        >
          <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700
                          flex flex-col items-center justify-center min-h-[220px]">
            {loading ? (
              <div className="flex flex-col items-center gap-3">
                <div className="w-10 h-10 border-4 border-blue-400
                                border-t-transparent rounded-full animate-spin" />
                <p className="text-slate-400 text-sm">Fetching prediction...</p>
              </div>
            ) : result !== null ? (
              <>
                <p className="text-slate-400 text-sm mb-4">
                  Predicted AQI for {city}
                </p>
                <AQIGauge aqi={result} />
              </>
            ) : (
              <p className="text-slate-500 text-sm">
                Adjust inputs and click Predict AQI
              </p>
            )}
          </div>

          {result !== null && !loading && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <HealthAdvisory bucket={bucket || getAQIBucket(result)} />
            </motion.div>
          )}
        </motion.div>

      </div>
    </div>
  );
}
