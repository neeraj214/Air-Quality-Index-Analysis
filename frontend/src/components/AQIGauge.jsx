import { motion } from 'framer-motion';
import { getAQIColor, getAQIBucket } from '../utils/aqiHelpers';

export default function AQIGauge({ aqi = 0 }) {
  const clamped = Math.min(Math.max(aqi, 0), 500);
  const pct     = clamped / 500;
  const color   = getAQIColor(clamped);
  const bucket  = getAQIBucket(clamped);

  const stroke       = 14;
  const radius       = 80;
  const normalizedR  = radius - stroke / 2;
  const circumference = Math.PI * normalizedR; // half-circle arc length
  const offset       = circumference * (1 - pct);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.75rem' }}>
      <svg width="200" height="120" viewBox="0 0 200 120">
        {/* Background arc */}
        <path
          d={`M ${stroke / 2} 100 A ${normalizedR} ${normalizedR} 0 0 1 ${200 - stroke / 2} 100`}
          fill="none"
          stroke="#1e293b"
          strokeWidth={stroke}
          strokeLinecap="round"
        />
        {/* Animated value arc */}
        <motion.path
          d={`M ${stroke / 2} 100 A ${normalizedR} ${normalizedR} 0 0 1 ${200 - stroke / 2} 100`}
          fill="none"
          stroke={color}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1.2, ease: 'easeOut' }}
        />
        {/* AQI number */}
        <text x="100" y="90" textAnchor="middle" fontSize="32" fontWeight="700" fill="white">
          {clamped}
        </text>
        <text x="100" y="110" textAnchor="middle" fontSize="11" fill="#94a3b8">
          out of 500
        </text>
      </svg>
      <span style={{
        padding: '0.25rem 1rem',
        borderRadius: '9999px',
        fontSize: '0.875rem',
        fontWeight: 600,
        backgroundColor: color + '33',
        color,
      }}>
        {bucket}
      </span>
    </div>
  );
}
