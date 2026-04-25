import { motion } from 'framer-motion';
import AQICard from '../components/AQICard';
import HealthAdvisory from '../components/HealthAdvisory';
import { cityStats } from '../data/cityData';

export default function Dashboard() {
  return (
    <div style={{ maxWidth: '80rem', margin: '0 auto', padding: '7rem 1.5rem 4rem' }}>

      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        style={{ marginBottom: '2.5rem' }}
      >
        <h1 style={{ fontSize: '2.25rem', fontWeight: 700, color: 'white', margin: 0 }}>
          Air Quality <span style={{ color: '#60a5fa' }}>Dashboard</span>
        </h1>
        <p style={{ color: '#94a3b8', marginTop: '0.5rem' }}>
          Real-time AQI overview across major Indian cities
        </p>
      </motion.div>

      {/* City Cards Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
        gap: '1.25rem',
        marginBottom: '2.5rem',
      }}>
        {cityStats.map((stat, i) => (
          <AQICard
            key={stat.city}
            city={stat.city}
            avgAQI={stat.avgAQI}
            maxAQI={stat.maxAQI}
            index={i}
          />
        ))}
      </div>

      {/* Health Advisories */}
      <motion.h2
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        style={{ fontSize: '1.25rem', fontWeight: 600, color: 'white', marginBottom: '1.25rem' }}
      >
        Health Advisories by City
      </motion.h2>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '1.25rem',
      }}>
        {cityStats.map((stat, i) => (
          <motion.div
            key={stat.city}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 + i * 0.1 }}
          >
            <p style={{ color: '#94a3b8', fontSize: '0.875rem', marginBottom: '0.5rem', fontWeight: 500 }}>
              {stat.city}
            </p>
            <HealthAdvisory bucket={stat.bucket} />
          </motion.div>
        ))}
      </div>
    </div>
  );
}
