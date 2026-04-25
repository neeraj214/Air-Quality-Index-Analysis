export default function Footer() {
  return (
    <footer style={{
      borderTop: '1px solid #334155',
      marginTop: '4rem',
      padding: '2rem',
      textAlign: 'center',
    }}>
      <p style={{ color: '#64748b', fontSize: '0.875rem', margin: 0 }}>
        AQI Analyser — Built with React + Tailwind + Framer Motion
      </p>
      <p style={{ color: '#475569', fontSize: '0.75rem', marginTop: '0.25rem' }}>
        Data source: CPCB India | ML Model: XGBoost + LightGBM
      </p>
    </footer>
  );
}
