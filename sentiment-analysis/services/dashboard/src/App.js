import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [alerts, setAlerts] = useState(0);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        // Use the actual accessible URL for your backend
        const response = await fetch('http://localhost:5000/alerts');
        
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        setAlerts(data.alerts);
        setError(null); // Clear previous errors
      } catch (err) {
        setError(err.message);
        console.error('Fetch error:', err);
      }
    };
    
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <h1>Sentiment Dashboard</h1>
      <div className="alert-count">
        Active Alerts: <span>{alerts}</span>
      </div>
      {error && <div className="error">Error: {error}</div>}
    </div>
  );
}

export default App;
