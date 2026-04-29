import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar    from './components/Navbar';
import Footer    from './components/Footer';
import Home      from './pages/Home';
import Dashboard from './pages/Dashboard';
import Predict   from './pages/Predict';
import Charts    from './pages/Charts';

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-900">
        <Navbar />
        <Routes>
          <Route path="/"          element={<Home />}      />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/predict"   element={<Predict />}   />
          <Route path="/charts"    element={<Charts />}    />
        </Routes>
        <Footer />
      </div>
    </BrowserRouter>
  );
}
