import { useEffect, useRef, useState } from 'react';
import { motion, useScroll,
         useTransform, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import CountUp from 'react-countup';
import {
  Wind, Activity, MapPin,
  ArrowRight, ChevronDown,
  AlertTriangle, Shield, Zap
} from 'lucide-react';

// -----------------------------------------------------------------------
// DATA
// -----------------------------------------------------------------------
const STATS = [
  { label: 'Cities Monitored',   value: 4,    suffix: '+',  icon: MapPin     },
  { label: 'ML Models Trained',  value: 8,    suffix: '',   icon: Zap        },
  { label: 'AQI Buckets',        value: 6,    suffix: '',   icon: Activity   },
  { label: 'Prediction Accuracy',value: 90,   suffix: '%',  icon: Shield     },
];

const FEATURES = [
  {
    icon : Wind,
    title: 'Real-time Prediction',
    desc : 'Get instant AQI predictions using pollutant readings powered by XGBoost and LightGBM models.',
    color: '#60a5fa',
  },
  {
    icon : Activity,
    title: 'City-wise Dashboard',
    desc : 'Compare air quality across Delhi, Bengaluru, Kolkata and Hyderabad with live visual charts.',
    color: '#34d399',
  },
  {
    icon : AlertTriangle,
    title: 'Health Advisories',
    desc : 'Receive instant health risk assessment and actionable advisories based on predicted AQI levels.',
    color: '#f9c74f',
  },
  {
    icon : Shield,
    title: 'SMOTE Balanced ML',
    desc : 'Models trained with SMOTE oversampling ensure reliable predictions even for rare severe AQI events.',
    color: '#f87171',
  },
];

const AQI_BUCKETS = [
  { label: 'Good',         range: '0–50',   color: '#2ecc71', delay: 0.1 },
  { label: 'Satisfactory', range: '51–100', color: '#a8d08d', delay: 0.2 },
  { label: 'Moderate',     range: '101–200',color: '#f9c74f', delay: 0.3 },
  { label: 'Poor',         range: '201–300',color: '#f77f00', delay: 0.4 },
  { label: 'Very Poor',    range: '301–400',color: '#d62828', delay: 0.5 },
  { label: 'Severe',       range: '401–500',color: '#6a040f', delay: 0.6 },
];

// -----------------------------------------------------------------------
// FLOATING PARTICLES BACKGROUND
// -----------------------------------------------------------------------
function Particles() {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {[...Array(18)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute rounded-full opacity-10"
          style={{
            width  : Math.random() * 80 + 20,
            height : Math.random() * 80 + 20,
            left   : `${Math.random() * 100}%`,
            top    : `${Math.random() * 100}%`,
            background: ['#60a5fa','#34d399','#f9c74f','#f87171'][i % 4],
          }}
          animate={{
            y      : [0, -30, 0],
            x      : [0, 15, 0],
            scale  : [1, 1.1, 1],
            opacity: [0.08, 0.18, 0.08],
          }}
          transition={{
            duration: Math.random() * 6 + 5,
            repeat  : Infinity,
            delay   : Math.random() * 3,
            ease    : 'easeInOut',
          }}
        />
      ))}
    </div>
  );
}

// -----------------------------------------------------------------------
// ANIMATED AQI GAUGE RING (hero decoration)
// -----------------------------------------------------------------------
function HeroGauge() {
  const [aqi, setAqi] = useState(245);

  useEffect(() => {
    const values = [72, 145, 312, 88, 245, 178, 420, 55];
    let i = 0;
    const interval = setInterval(() => {
      i = (i + 1) % values.length;
      setAqi(values[i]);
    }, 2200);
    return () => clearInterval(interval);
  }, []);

  const getColor = (v) => {
    if (v <= 50)  return '#2ecc71';
    if (v <= 100) return '#a8d08d';
    if (v <= 200) return '#f9c74f';
    if (v <= 300) return '#f77f00';
    if (v <= 400) return '#d62828';
    return '#6a040f';
  };

  const getBucket = (v) => {
    if (v <= 50)  return 'Good';
    if (v <= 100) return 'Satisfactory';
    if (v <= 200) return 'Moderate';
    if (v <= 300) return 'Poor';
    if (v <= 400) return 'Very Poor';
    return 'Severe';
  };

  const color  = getColor(aqi);
  const pct    = aqi / 500;
  const r      = 90;
  const stroke = 16;
  const norm   = r - stroke / 2;
  const circ   = Math.PI * norm;
  const offset = circ * (1 - pct);

  return (
    <motion.div
      className="relative flex items-center justify-center"
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1  }}
      transition={{ duration: 0.8, delay: 0.4 }}
    >
      {/* Outer glow ring */}
      <motion.div
        className="absolute rounded-full"
        style={{
          width           : 260,
          height          : 260,
          background      : `radial-gradient(circle, ${color}22 0%, transparent 70%)`,
          boxShadow       : `0 0 60px ${color}44`,
        }}
        animate={{ scale: [1, 1.05, 1] }}
        transition={{ duration: 2.5, repeat: Infinity, ease: 'easeInOut' }}
      />

      {/* SVG Gauge */}
      <svg width="240" height="140" viewBox="0 0 240 140">
        {/* Background arc */}
        <path
          d={`M ${stroke/2} 120 A ${norm} ${norm} 0 0 1 ${240-stroke/2} 120`}
          fill="none" stroke="#1e293b"
          strokeWidth={stroke} strokeLinecap="round"
        />
        {/* Value arc */}
        <motion.path
          d={`M ${stroke/2} 120 A ${norm} ${norm} 0 0 1 ${240-stroke/2} 120`}
          fill="none"
          stroke={color}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={circ}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1.0, ease: 'easeOut' }}
        />
        {/* AQI number */}
        <motion.text
          x="120" y="105"
          textAnchor="middle"
          fontSize="42"
          fontWeight="800"
          fill="white"
          animate={{ opacity: [0, 1] }}
          transition={{ duration: 0.4 }}
          key={aqi}
        >
          {aqi}
        </motion.text>
        <text x="120" y="128" textAnchor="middle"
              fontSize="11" fill="#94a3b8">
          AQI Index
        </text>
      </svg>

      {/* Bucket badge */}
      <AnimatePresence mode="wait">
        <motion.div
          key={getBucket(aqi)}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          exit   ={{ opacity: 0, y: -8 }}
          transition={{ duration: 0.3 }}
          className="absolute bottom-0 px-5 py-1.5 rounded-full
                     text-sm font-bold"
          style={{
            backgroundColor: color + '33',
            color,
            border: `1px solid ${color}66`,
          }}
        >
          {getBucket(aqi)}
        </motion.div>
      </AnimatePresence>
    </motion.div>
  );
}

// -----------------------------------------------------------------------
// MAIN HOME COMPONENT
// -----------------------------------------------------------------------
export default function Home() {
  const navigate    = useNavigate();
  const heroRef     = useRef(null);
  const { scrollY } = useScroll();
  const heroOpacity = useTransform(scrollY, [0, 400], [1, 0]);
  const heroY       = useTransform(scrollY, [0, 400], [0, -80]);

  return (
    <div className="min-h-screen bg-slate-900 overflow-x-hidden">

      {/* ================================================================
          HERO SECTION
      ================================================================ */}
      <section
        ref={heroRef}
        className="relative min-h-screen flex items-center
                   justify-center overflow-hidden"
      >
        <Particles />

        {/* Gradient background blobs */}
        <div className="absolute top-20 left-10 w-72 h-72 rounded-full
                        bg-blue-600 opacity-10 blur-3xl pointer-events-none" />
        <div className="absolute bottom-20 right-10 w-96 h-96 rounded-full
                        bg-emerald-600 opacity-10 blur-3xl pointer-events-none" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2
                        -translate-y-1/2 w-[600px] h-[600px] rounded-full
                        bg-indigo-900 opacity-20 blur-3xl pointer-events-none" />

        <motion.div
          style={{ opacity: heroOpacity, y: heroY }}
          className="relative z-10 max-w-7xl mx-auto px-6 pt-24
                     grid grid-cols-1 lg:grid-cols-2 gap-16
                     items-center"
        >
          {/* Left — Text */}
          <div>
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="inline-flex items-center gap-2 px-4 py-2
                         rounded-full border border-blue-500/40
                         bg-blue-500/10 text-blue-400 text-sm
                         font-medium mb-6"
            >
              <span className="w-2 h-2 rounded-full bg-blue-400
                               animate-pulse" />
              ML-Powered Air Quality Analysis
            </motion.div>

            {/* Headline */}
            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="text-5xl lg:text-6xl font-extrabold
                         text-white leading-tight mb-6"
            >
              Predict
              <span className="block text-transparent bg-clip-text
                               bg-gradient-to-r from-blue-400
                               to-emerald-400">
                Air Quality
              </span>
              Before It Harms
            </motion.h1>

            {/* Subtitle */}
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="text-slate-400 text-lg leading-relaxed mb-8
                         max-w-lg"
            >
              Advanced AQI forecasting for Delhi, Bengaluru, Kolkata
              and Hyderabad using XGBoost and LightGBM models trained
              on real CPCB pollutant data.
            </motion.p>

            {/* CTA Buttons */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="flex flex-wrap gap-4"
            >
              <motion.button
                whileHover={{ scale: 1.04 }}
                whileTap ={{ scale: 0.97 }}
                onClick={() => navigate('/predict')}
                className="flex items-center gap-2 px-7 py-3.5
                           rounded-xl font-semibold text-white
                           bg-gradient-to-r from-blue-600 to-blue-500
                           hover:from-blue-500 hover:to-blue-400
                           shadow-lg shadow-blue-500/25
                           transition-all duration-200"
              >
                Predict AQI Now
                <ArrowRight size={18} />
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.04 }}
                whileTap ={{ scale: 0.97 }}
                onClick={() => navigate('/dashboard')}
                className="flex items-center gap-2 px-7 py-3.5
                           rounded-xl font-semibold text-slate-300
                           border border-slate-600
                           hover:border-slate-400 hover:text-white
                           transition-all duration-200"
              >
                View Dashboard
              </motion.button>
            </motion.div>
          </div>

          {/* Right — Animated Gauge */}
          <div className="flex justify-center">
            <HeroGauge />
          </div>
        </motion.div>

        {/* Scroll indicator */}
        <motion.div
          className="absolute bottom-8 left-1/2 -translate-x-1/2
                     flex flex-col items-center gap-1 text-slate-500"
          animate={{ y: [0, 8, 0] }}
          transition={{ duration: 1.8, repeat: Infinity }}
        >
          <span className="text-xs">Scroll to explore</span>
          <ChevronDown size={18} />
        </motion.div>
      </section>

      {/* ================================================================
          STATS SECTION
      ================================================================ */}
      <section className="py-20 border-y border-slate-800
                          bg-slate-900/80 backdrop-blur-sm">
        <div className="max-w-5xl mx-auto px-6
                        grid grid-cols-2 lg:grid-cols-4 gap-8">
          {STATS.map((stat, i) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1, duration: 0.5 }}
              className="flex flex-col items-center text-center gap-3"
            >
              <div className="w-12 h-12 rounded-xl bg-blue-500/10
                              border border-blue-500/20 flex items-center
                              justify-center text-blue-400">
                <stat.icon size={22} />
              </div>
              <div className="text-4xl font-extrabold text-white">
                <CountUp
                  end={stat.value}
                  duration={2.5}
                  suffix={stat.suffix}
                  enableScrollSpy
                  scrollSpyOnce
                />
              </div>
              <p className="text-slate-400 text-sm">{stat.label}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ================================================================
          AQI SCALE SECTION
      ================================================================ */}
      <section className="py-24 max-w-5xl mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-14"
        >
          <h2 className="text-3xl font-bold text-white mb-3">
            Understanding the{' '}
            <span className="text-transparent bg-clip-text
                             bg-gradient-to-r from-blue-400
                             to-emerald-400">
              AQI Scale
            </span>
          </h2>
          <p className="text-slate-400 max-w-xl mx-auto">
            AQI ranges from 0 to 500. Higher values indicate
            greater levels of air pollution and health concern.
          </p>
        </motion.div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {AQI_BUCKETS.map((b) => (
            <motion.div
              key={b.label}
              initial={{ opacity: 0, scale: 0.85 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: b.delay, duration: 0.4 }}
              whileHover={{ scale: 1.06, y: -4 }}
              className="rounded-2xl p-5 flex flex-col items-center
                         gap-3 border cursor-default"
              style={{
                backgroundColor: b.color + '15',
                borderColor    : b.color + '40',
              }}
            >
              <div
                className="w-10 h-10 rounded-full"
                style={{ backgroundColor: b.color }}
              />
              <p className="text-white font-semibold text-sm text-center">
                {b.label}
              </p>
              <p className="text-xs font-mono" style={{ color: b.color }}>
                {b.range}
              </p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ================================================================
          FEATURES SECTION
      ================================================================ */}
      <section className="py-24 bg-slate-800/40 border-y border-slate-800">
        <div className="max-w-6xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-14"
          >
            <h2 className="text-3xl font-bold text-white mb-3">
              What This{' '}
              <span className="text-transparent bg-clip-text
                               bg-gradient-to-r from-blue-400
                               to-emerald-400">
                Platform Does
              </span>
            </h2>
            <p className="text-slate-400 max-w-xl mx-auto">
              End-to-end air quality intelligence from raw pollutant
              data to actionable health decisions.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 sm:grid-cols-2
                          lg:grid-cols-4 gap-6">
            {FEATURES.map((f, i) => (
              <motion.div
                key={f.title}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.12, duration: 0.5 }}
                whileHover={{ y: -6 }}
                className="bg-slate-800 rounded-2xl p-6 border
                           border-slate-700 hover:border-slate-500
                           transition-all duration-300 group"
              >
                <div
                  className="w-12 h-12 rounded-xl flex items-center
                             justify-center mb-5"
                  style={{
                    backgroundColor: f.color + '20',
                    border: `1px solid ${f.color}40`,
                  }}
                >
                  <f.icon size={22} style={{ color: f.color }} />
                </div>
                <h3 className="text-white font-semibold text-base mb-2
                               group-hover:text-blue-400
                               transition-colors duration-200">
                  {f.title}
                </h3>
                <p className="text-slate-400 text-sm leading-relaxed">
                  {f.desc}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ================================================================
          CTA SECTION
      ================================================================ */}
      <section className="py-28 max-w-4xl mx-auto px-6 text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          {/* Glow */}
          <div className="absolute left-1/2 -translate-x-1/2 w-96 h-40
                          bg-blue-600 opacity-10 blur-3xl
                          pointer-events-none" />

          <h2 className="text-4xl font-extrabold text-white mb-4">
            Ready to Check Your{' '}
            <span className="text-transparent bg-clip-text
                             bg-gradient-to-r from-blue-400
                             to-emerald-400">
              Air Quality?
            </span>
          </h2>
          <p className="text-slate-400 text-lg mb-10">
            Enter pollutant values and get an instant ML-powered
            AQI prediction with health advisory.
          </p>

          <div className="flex flex-wrap justify-center gap-4">
            <motion.button
              whileHover={{ scale: 1.04 }}
              whileTap ={{ scale: 0.97 }}
              onClick={() => navigate('/predict')}
              className="flex items-center gap-2 px-8 py-4
                         rounded-xl font-semibold text-white text-lg
                         bg-gradient-to-r from-blue-600 to-emerald-500
                         hover:from-blue-500 hover:to-emerald-400
                         shadow-xl shadow-blue-500/20
                         transition-all duration-200"
            >
              Start Predicting
              <ArrowRight size={20} />
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.04 }}
              whileTap ={{ scale: 0.97 }}
              onClick={() => navigate('/charts')}
              className="flex items-center gap-2 px-8 py-4
                         rounded-xl font-semibold text-slate-300
                         text-lg border border-slate-600
                         hover:border-slate-400 hover:text-white
                         transition-all duration-200"
            >
              Explore Charts
            </motion.button>
          </div>
        </motion.div>
      </section>

    </div>
  );
}
