import React, { useState } from 'react';
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
  const [results, setResults] = useState<TriageResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleTriageComplete = (data: TriageResponse) => {
    setResults(data);
    setError(null);
  };

  const handleError = (errorMessage: string) => {
    setError(errorMessage);
    setResults(null);
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Defect Analysis & Triaging Tool</h1>
        <p>Upload your log file and analyze known errors</p>
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
