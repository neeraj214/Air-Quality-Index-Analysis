import { motion } from 'framer-motion';
import { getHealthAdvisory, getAQIColor } from '../utils/aqiHelpers';

const bucketToAQI = {
  Good: 25, Satisfactory: 75, Moderate: 150,
  Poor: 250, 'Very Poor': 350, Severe: 450,
};

export default function HealthAdvisory({ bucket }) {
  const advisory = getHealthAdvisory(bucket);
  const color    = getAQIColor(bucketToAQI[bucket] ?? 150);

  return (
    <motion.div
      key={bucket}
      initial={{ opacity: 0, scale: 0.97 }}
      animate={{ opacity: 1, scale: 1    }}
      transition={{ duration: 0.4 }}
      style={{
        borderRadius: '1rem',
        padding: '1.25rem',
        border: `1px solid ${color}55`,
        backgroundColor: color + '15',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
        <span style={{ fontSize: '1.875rem' }}>{advisory.icon}</span>
        <div>
          <p style={{ color: 'white', fontWeight: 600, margin: 0 }}>Health Advisory</p>
          <p style={{ fontSize: '0.75rem', fontWeight: 500, color, margin: 0 }}>
            Risk Level: {advisory.risk}
          </p>
        </div>
      </div>
      <p style={{ color: '#cbd5e1', fontSize: '0.875rem', lineHeight: 1.6, margin: 0 }}>
        {advisory.message}
      </p>
    </motion.div>
  );
}
