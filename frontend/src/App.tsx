import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Login from './components/Login';
import UploadForm from './components/UploadForm';
import ResultsDisplay from './components/ResultsDisplay';
import './App.css';

export interface TriageResult {
  line_number: number;
  log_line: string;
  interpretation: string;
}

export interface TriageResponse {
  total_errors: number;
  displayed_errors: number;
  results: TriageResult[];
  log_filename: string;
  mappings_count: number;
}

const App: React.FC = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState<string | null>(null);
  const [authChecking, setAuthChecking] = useState(true);
  const [results, setResults] = useState<TriageResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Check authentication status on mount
  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await axios.get('/api/check-auth', {
        withCredentials: true
      });
      if (response.data.authenticated) {
        setIsAuthenticated(true);
        setUsername(response.data.username);
      }
    } catch (err) {
      // Not authenticated, stay on login page
      setIsAuthenticated(false);
    } finally {
      setAuthChecking(false);
    }
  };

  const handleLoginSuccess = (user: string) => {
    setIsAuthenticated(true);
    setUsername(user);
  };

  const handleLogout = async () => {
    try {
      await axios.post('/api/logout', {}, {
        withCredentials: true
      });
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      setIsAuthenticated(false);
      setUsername(null);
      setResults(null);
      setError(null);
    }
  };

  const handleTriageComplete = (data: TriageResponse) => {
    setResults(data);
    setError(null);
  };

  const handleError = (errorMessage: string) => {
    // Check if it's an authentication error
    if (errorMessage.includes('Authentication required') || errorMessage.includes('401')) {
      setIsAuthenticated(false);
      setUsername(null);
      setError('Session expired. Please log in again.');
    } else {
      setError(errorMessage);
      setResults(null);
    }
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
  };

  // Show loading while checking auth
  if (authChecking) {
    return (
      <div className="App">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  // Show login page if not authenticated
  if (!isAuthenticated) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  // Show main app if authenticated
  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <div>
            <h1>Defect Analysis & Triaging Tool</h1>
            <p>Upload your log file and analyze known errors</p>
          </div>
          <div className="header-user">
            <span className="welcome-text">Welcome, {username}</span>
            <button onClick={handleLogout} className="logout-button">
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="App-main">
        <UploadForm
          onTriageComplete={handleTriageComplete}
          onError={handleError}
          onLoadingChange={setLoading}
          onReset={handleReset}
        />

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Analyzing log file...</p>
          </div>
        )}

        {error && (
          <div className="error-message">
            <h3>Error</h3>
            <p>{error}</p>
          </div>
        )}

        {results && !loading && (
          <ResultsDisplay results={results} onReset={handleReset} />
        )}
      </main>

      <footer className="App-footer">
        <p>Defect Analysis & Triaging Tool v1.0</p>
      </footer>
    </div>
  );
};

export default App;
