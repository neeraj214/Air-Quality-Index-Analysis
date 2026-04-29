import { motion, AnimatePresence } from 'framer-motion';
import { Link, useLocation }       from 'react-router-dom';
import { Wind, Menu, X }           from 'lucide-react';
import { useState }                from 'react';

const navLinks = [
  { path: '/',          label: 'Home'      },
  { path: '/dashboard', label: 'Dashboard' },
  { path: '/predict',   label: 'Predict'   },
  { path: '/charts',    label: 'Charts'    },
];

export default function Navbar() {
  const location  = useLocation();
  const [open, setOpen] = useState(false);

  return (
    <motion.nav
      initial={{ y: -60, opacity: 0 }}
      animate={{ y: 0,   opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="fixed top-0 left-0 right-0 z-50 bg-slate-900/80
                 backdrop-blur-md border-b border-slate-700/60"
    >
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center
                      justify-between">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-blue-500/20
                          border border-blue-500/40 flex items-center
                          justify-center">
            <Wind className="text-blue-400" size={18} />
          </div>
          <span className="text-white font-bold text-lg tracking-tight">
            AQI <span className="text-blue-400">Analyser</span>
          </span>
        </Link>

        {/* Desktop links */}
        <div className="hidden md:flex items-center gap-1">
          {navLinks.map(link => {
            const active = location.pathname === link.path;
            return (
              <Link
                key={link.path}
                to={link.path}
                className={`relative px-4 py-2 rounded-lg text-sm
                  font-medium transition-all duration-200
                  ${active
                    ? 'text-white bg-slate-700/60'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800'
                  }`}
              >
                {link.label}
                {active && (
                  <motion.div
                    layoutId="nav-indicator"
                    className="absolute bottom-0 left-1/2 -translate-x-1/2
                               w-4 h-0.5 bg-blue-400 rounded-full"
                  />
                )}
              </Link>
            );
          })}

          <Link
            to="/predict"
            className="ml-3 px-4 py-2 rounded-lg text-sm font-semibold
                       text-white bg-blue-600 hover:bg-blue-500
                       transition-colors duration-200"
          >
            Predict Now
          </Link>
        </div>

        {/* Mobile hamburger */}
        <button
          className="md:hidden text-slate-400 hover:text-white"
          onClick={() => setOpen(!open)}
        >
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>

      {/* Mobile menu */}
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit   ={{ opacity: 0, height: 0 }}
            className="md:hidden border-t border-slate-700/60
                       bg-slate-900/95 backdrop-blur-md px-6 py-4
                       flex flex-col gap-2"
          >
            {navLinks.map(link => (
              <Link
                key={link.path}
                to={link.path}
                onClick={() => setOpen(false)}
                className={`px-4 py-2.5 rounded-lg text-sm font-medium
                  transition-colors duration-200
                  ${location.pathname === link.path
                    ? 'text-white bg-slate-700'
                    : 'text-slate-400 hover:text-white'
                  }`}
              >
                {link.label}
              </Link>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.nav>
  );
}
