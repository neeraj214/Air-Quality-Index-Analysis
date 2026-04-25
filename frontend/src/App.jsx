import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar    from './components/Navbar';
import Footer    from './components/Footer';
import Dashboard from './pages/Dashboard';
import Predict   from './pages/Predict';
import Charts    from './pages/Charts';

export default function App() {
  return (
    <BrowserRouter>
      <div style={{ minHeight: '100vh', backgroundColor: '#0f172a' }}>
        <Navbar />
        <Routes>
          <Route path="/"        element={<Dashboard />} />
          <Route path="/predict" element={<Predict />}   />
          <Route path="/charts"  element={<Charts />}    />
        </Routes>
        <Footer />
      </div>
    </BrowserRouter>
  );
}
