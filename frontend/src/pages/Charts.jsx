import { motion } from 'framer-motion';
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis,
  CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from 'recharts';
import { monthlyAQI, pollutantData } from '../data/cityData';

const CITY_COLORS = {
  Delhi:     '#f77f00',
  Bengaluru: '#2ecc71',
  Kolkata:   '#f9c74f',
  Hyderabad: '#60a5fa',
};

const tooltipStyle = {
  contentStyle: {
    backgroundColor: '#1e293b',
    border: '1px solid #334155',
    borderRadius: '0.75rem',
    color: '#f1f5f9',
  },
};

export default function Charts() {
  return (
    <div style={{ maxWidth: '80rem', margin: '0 auto', padding: '7rem 1.5rem 4rem' }}>

      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        style={{ marginBottom: '2.5rem' }}
      >
        <h1 style={{ fontSize: '2.25rem', fontWeight: 700, color: 'white', margin: 0 }}>
          AQI <span style={{ color: '#60a5fa' }}>Charts</span>
        </h1>
        <p style={{ color: '#94a3b8', marginTop: '0.5rem' }}>
          Visual trends and pollutant comparisons across cities
        </p>
      </motion.div>

      {/* Monthly AQI Trend */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        style={{
          backgroundColor: '#1e293b',
          borderRadius: '1rem',
          padding: '1.5rem',
          border: '1px solid #334155',
          marginBottom: '2rem',
        }}
      >
        <h2 style={{ color: 'white', fontWeight: 600, fontSize: '1.125rem', marginBottom: '1.5rem', marginTop: 0 }}>
          Monthly AQI Trend (2023)
        </h2>
        <ResponsiveContainer width="100%" height={320}>
          <LineChart data={monthlyAQI}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey="month" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip {...tooltipStyle} />
            <Legend />
            {Object.entries(CITY_COLORS).map(([city, color]) => (
              <Line
                key={city}
                type="monotone"
                dataKey={city}
                stroke={color}
                strokeWidth={2.5}
                dot={false}
                activeDot={{ r: 5 }}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </motion.div>

      {/* Pollutant Comparison Bar Chart */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        style={{
          backgroundColor: '#1e293b',
          borderRadius: '1rem',
          padding: '1.5rem',
          border: '1px solid #334155',
        }}
      >
        <h2 style={{ color: 'white', fontWeight: 600, fontSize: '1.125rem', marginBottom: '1.5rem', marginTop: 0 }}>
          Pollutant Levels by City
        </h2>
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={pollutantData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey="pollutant" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip {...tooltipStyle} />
            <Legend />
            {Object.entries(CITY_COLORS).map(([city, color]) => (
              <Bar key={city} dataKey={city} fill={color} radius={[4, 4, 0, 0]} />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </motion.div>

    </div>
  );
}
