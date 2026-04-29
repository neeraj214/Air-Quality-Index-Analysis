import axios from 'axios';

const api = axios.create({
  baseURL : import.meta.env.VITE_API_URL || 'http://localhost:7860',
  timeout : 60000,  // 60s timeout — HF Spaces can be slow on cold start
  headers : {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    console.log(`→ ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED') {
      console.error('Timeout — Space may be waking up. Try again in 30s.');
    }
    return Promise.reject(error);
  }
);

export default api;
