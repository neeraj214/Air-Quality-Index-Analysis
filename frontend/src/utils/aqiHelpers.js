export const getAQIColor = (aqi) => {
  if (aqi <= 50)  return '#2ecc71';
  if (aqi <= 100) return '#a8d08d';
  if (aqi <= 200) return '#f9c74f';
  if (aqi <= 300) return '#f77f00';
  if (aqi <= 400) return '#d62828';
  return '#6a040f';
};

export const getAQIBucket = (aqi) => {
  if (aqi <= 50)  return 'Good';
  if (aqi <= 100) return 'Satisfactory';
  if (aqi <= 200) return 'Moderate';
  if (aqi <= 300) return 'Poor';
  if (aqi <= 400) return 'Very Poor';
  return 'Severe';
};

export const getHealthAdvisory = (bucket) => {
  const advisories = {
    Good:         { message: 'Air quality is satisfactory. Enjoy outdoor activities.', icon: '✅', risk: 'Minimal' },
    Satisfactory: { message: 'Air quality is acceptable. Sensitive groups should limit prolonged exertion.', icon: '🟡', risk: 'Low' },
    Moderate:     { message: 'Members of sensitive groups may experience health effects.', icon: '⚠️', risk: 'Moderate' },
    Poor:         { message: 'Everyone may begin to experience health effects. Limit outdoor activity.', icon: '🔶', risk: 'High' },
    'Very Poor':  { message: 'Health alert: everyone may experience serious health effects.', icon: '🔴', risk: 'Very High' },
    Severe:       { message: 'Emergency conditions. Avoid all outdoor activity.', icon: '☠️', risk: 'Hazardous' },
  };
  return advisories[bucket] || advisories['Moderate'];
};

export const CITIES = ['Delhi', 'Bengaluru', 'Kolkata', 'Hyderabad'];

export const POLLUTANTS = [
  { key: 'PM2.5', label: 'PM2.5', unit: 'µg/m³', min: 0,  max: 300 },
  { key: 'PM10',  label: 'PM10',  unit: 'µg/m³', min: 0,  max: 500 },
  { key: 'NO2',   label: 'NO₂',   unit: 'µg/m³', min: 0,  max: 150 },
  { key: 'CO',    label: 'CO',    unit: 'mg/m³',  min: 0,  max: 50  },
  { key: 'SO2',   label: 'SO₂',   unit: 'µg/m³', min: 0,  max: 100 },
  { key: 'O3',    label: 'O₃',    unit: 'µg/m³', min: 0,  max: 200 },
];
