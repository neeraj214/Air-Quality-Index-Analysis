import { motion } from 'framer-motion';
import { getAQIColor, getAQIBucket } from '../utils/aqiHelpers';

export default function AQICard({ city, avgAQI, maxAQI, index }) {
  const color  = getAQIColor(avgAQI);
  const bucket = getAQIBucket(avgAQI);

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0  }}
      transition={{ delay: index * 0.1, duration: 0.5 }}
      style={{
        backgroundColor: '#1e293b',
        borderRadius: '1rem',
        padding: '1.25rem',
        border: '1px solid #334155',
        transition: 'border-color 0.3s',
        cursor: 'default',
      }}
      whileHover={{ borderColor: '#3b82f6', scale: 1.02 }}
    >
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
        <h3 style={{ color: 'white', fontWeight: 600, fontSize: '1.125rem', margin: 0 }}>{city}</h3>
        <span style={{
          fontSize: '0.75rem',
          fontWeight: 600,
          padding: '0.25rem 0.75rem',
          borderRadius: '9999px',
          backgroundColor: color + '22',
          color,
        }}>
          {bucket}
        </span>
      </div>

      <div style={{ display: 'flex', alignItems: 'flex-end', gap: '1.5rem' }}>
        <div>
          <p style={{ color: '#94a3b8', fontSize: '0.75rem', marginBottom: '0.25rem' }}>Avg AQI</p>
          <p style={{ fontSize: '1.875rem', fontWeight: 700, color, margin: 0 }}>{avgAQI}</p>
        </div>
        <div>
          <p style={{ color: '#94a3b8', fontSize: '0.75rem', marginBottom: '0.25rem' }}>Peak AQI</p>
          <p style={{ fontSize: '1.25rem', fontWeight: 600, color: '#cbd5e1', margin: 0 }}>{maxAQI}</p>
        </div>
      </div>

      {/* Mini progress bar */}
      <div style={{
        marginTop: '1rem',
        height: '6px',
        backgroundColor: '#334155',
        borderRadius: '9999px',
        overflow: 'hidden',
      }}>
        <motion.div
          style={{ height: '100%', borderRadius: '9999px', backgroundColor: color }}
          initial={{ width: 0 }}
          animate={{ width: `${(avgAQI / 500) * 100}%` }}
          transition={{ duration: 1, ease: 'easeOut', delay: index * 0.1 }}
        />
      </div>
    </motion.div>
  );
}
