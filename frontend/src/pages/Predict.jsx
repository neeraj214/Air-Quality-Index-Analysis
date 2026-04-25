import { useState } from 'react';
import { motion } from 'framer-motion';
import AQIGauge from '../components/AQIGauge';
import HealthAdvisory from '../components/HealthAdvisory';
import { CITIES, POLLUTANTS, getAQIBucket } from '../utils/aqiHelpers';

const defaultInputs = {
  'PM2.5': 60, PM10: 100, NO2: 40, CO: 1.5, SO2: 20, O3: 50,
};

export default function Predict() {
  const [city,    setCity]    = useState('Delhi');
  const [inputs,  setInputs]  = useState(defaultInputs);
  const [result,  setResult]  = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSlider = (key, value) =>
    setInputs(prev => ({ ...prev, [key]: Number(value) }));

  const handlePredict = async () => {
    setLoading(true);
    // TODO: replace with real FastAPI call when backend is ready
    // const res = await axios.post('http://localhost:8000/predict', { city, ...inputs });
    // setResult(res.data.aqi);
    await new Promise(r => setTimeout(r, 1000)); // simulate API delay
    const mock = Math.round(
      inputs['PM2.5'] * 1.8 + inputs.PM10 * 0.5 + inputs.NO2 * 1.2
    );
    setResult(Math.min(mock, 500));
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: '64rem', margin: '0 auto', padding: '7rem 1.5rem 4rem' }}>

      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        style={{ marginBottom: '2.5rem' }}
      >
        <h1 style={{ fontSize: '2.25rem', fontWeight: 700, color: 'white', margin: 0 }}>
          Predict <span style={{ color: '#60a5fa' }}>AQI</span>
        </h1>
        <p style={{ color: '#94a3b8', marginTop: '0.5rem' }}>
          Enter pollutant readings to get an AQI prediction
        </p>
      </motion.div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '2rem',
      }}>

        {/* Input Panel */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          style={{
            backgroundColor: '#1e293b',
            borderRadius: '1rem',
            padding: '1.5rem',
            border: '1px solid #334155',
          }}
        >
          {/* City Selector */}
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ color: '#94a3b8', fontSize: '0.875rem', display: 'block', marginBottom: '0.5rem' }}>
              City
            </label>
            <select
              value={city}
              onChange={e => setCity(e.target.value)}
              style={{
                width: '100%',
                backgroundColor: '#334155',
                color: 'white',
                borderRadius: '0.75rem',
                padding: '0.625rem 1rem',
                border: '1px solid #475569',
                outline: 'none',
                fontSize: '0.875rem',
              }}
            >
              {CITIES.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>

          {/* Pollutant Sliders */}
          {POLLUTANTS.map(p => (
            <div key={p.key} style={{ marginBottom: '1.25rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                <label style={{ color: '#cbd5e1', fontSize: '0.875rem' }}>{p.label}</label>
                <span style={{ color: '#60a5fa', fontSize: '0.875rem', fontWeight: 500 }}>
                  {inputs[p.key]} {p.unit}
                </span>
              </div>
              <input
                type="range"
                min={p.min}
                max={p.max}
                step={p.key === 'CO' ? 0.1 : 1}
                value={inputs[p.key]}
                onChange={e => handleSlider(p.key, e.target.value)}
                style={{ width: '100%', accentColor: '#60a5fa' }}
              />
              <div style={{ display: 'flex', justifyContent: 'space-between', color: '#475569', fontSize: '0.75rem' }}>
                <span>{p.min}</span><span>{p.max}</span>
              </div>
            </div>
          ))}

          <button
            onClick={handlePredict}
            disabled={loading}
            style={{
              width: '100%',
              marginTop: '1rem',
              padding: '0.75rem',
              borderRadius: '0.75rem',
              fontWeight: 600,
              color: 'white',
              backgroundColor: loading ? '#1d4ed8' : '#2563eb',
              border: 'none',
              cursor: loading ? 'not-allowed' : 'pointer',
              opacity: loading ? 0.6 : 1,
              fontSize: '1rem',
              transition: 'background-color 0.2s',
            }}
          >
            {loading ? 'Predicting...' : 'Predict AQI →'}
          </button>
        </motion.div>

        {/* Result Panel */}
        <motion.div
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}
        >
          <div style={{
            backgroundColor: '#1e293b',
            borderRadius: '1rem',
            padding: '1.5rem',
            border: '1px solid #334155',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: '220px',
          }}>
            {result !== null ? (
              <>
                <p style={{ color: '#94a3b8', fontSize: '0.875rem', marginBottom: '1rem' }}>
                  Predicted AQI for {city}
                </p>
                <AQIGauge aqi={result} />
              </>
            ) : (
              <p style={{ color: '#475569', fontSize: '0.875rem' }}>
                Adjust inputs and click Predict AQI
              </p>
            )}
          </div>

          {result !== null && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <HealthAdvisory bucket={getAQIBucket(result)} />
            </motion.div>
          )}
        </motion.div>

      </div>
    </div>
  );
}
