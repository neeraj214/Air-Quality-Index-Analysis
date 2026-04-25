import { motion } from 'framer-motion';
import { Link, useLocation } from 'react-router-dom';
import { Wind } from 'lucide-react';

const navLinks = [
  { path: '/',        label: 'Dashboard' },
  { path: '/predict', label: 'Predict AQI' },
  { path: '/charts',  label: 'Charts'     },
];

export default function Navbar() {
  const location = useLocation();

  return (
    <motion.nav
      initial={{ y: -60, opacity: 0 }}
      animate={{ y: 0,   opacity: 1 }}
      transition={{ duration: 0.5 }}
      style={{
        position: 'fixed',
        top: 0, left: 0, right: 0,
        zIndex: 50,
        backgroundColor: 'rgba(15, 23, 42, 0.85)',
        backdropFilter: 'blur(12px)',
        borderBottom: '1px solid #334155',
      }}
    >
      <div style={{
        maxWidth: '80rem',
        margin: '0 auto',
        padding: '1rem 1.5rem',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <Wind color="#60a5fa" size={24} />
          <span style={{ color: 'white', fontWeight: 700, fontSize: '1.125rem', letterSpacing: '-0.025em' }}>
            AQI <span style={{ color: '#60a5fa' }}>Analyser</span>
          </span>
        </div>
        <div style={{ display: 'flex', gap: '1.5rem' }}>
          {navLinks.map(link => (
            <Link
              key={link.path}
              to={link.path}
              style={{
                fontSize: '0.875rem',
                fontWeight: 500,
                textDecoration: 'none',
                color: location.pathname === link.path ? '#60a5fa' : '#94a3b8',
                borderBottom: location.pathname === link.path ? '2px solid #60a5fa' : '2px solid transparent',
                paddingBottom: '2px',
                transition: 'color 0.2s',
              }}
            >
              {link.label}
            </Link>
          ))}
        </div>
      </div>
    </motion.nav>
  );
}
