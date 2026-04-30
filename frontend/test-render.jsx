import React from 'react';
import { renderToString } from 'react-dom/server';
import Home from './src/pages/Home.jsx';
import { BrowserRouter } from 'react-router-dom';

try {
  console.log(renderToString(<BrowserRouter><Home /></BrowserRouter>));
  console.log('SUCCESS');
} catch (e) {
  console.error('ERROR:', e.message);
}
