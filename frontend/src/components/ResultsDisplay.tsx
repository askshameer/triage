import React, { useState } from 'react';
import { TriageResponse } from '../App';
import './ResultsDisplay.css';

interface ResultsDisplayProps {
  results: TriageResponse;
  onReset: () => void;
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ results, onReset }) => {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  const toggleExpand = (index: number) => {
    setExpandedIndex(expandedIndex === index ? null : index);
  };

  const exportToJSON = () => {
    const dataStr = JSON.stringify(results, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
    const exportFileDefaultName = `triage_results_${results.log_filename}_${new Date().getTime()}.json`;

    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  const exportToCSV = () => {
    let csv = 'Line Number,Log Line,Interpretation\n';
    results.results.forEach(result => {
      const logLine = result.log_line.replace(/"/g, '""');
      const interpretation = result.interpretation.replace(/"/g, '""');
      csv += `${result.line_number},"${logLine}","${interpretation}"\n`;
    });

    const dataUri = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv);
    const exportFileDefaultName = `triage_results_${results.log_filename}_${new Date().getTime()}.csv`;

    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  return (
    <div className="results-container">
      <div className="results-header">
        <div className="results-summary">
          <h2>Analysis Results</h2>
          <div className="summary-stats">
            <div className="stat-item">
              <span className="stat-label">Log File:</span>
              <span className="stat-value">{results.log_filename}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Total Errors Found:</span>
              <span className="stat-value highlight">{results.total_errors}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Displayed:</span>
              <span className="stat-value">{results.displayed_errors}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Error Mappings Loaded:</span>
              <span className="stat-value">{results.mappings_count}</span>
            </div>
          </div>
        </div>

        <div className="results-actions">
          <button onClick={exportToJSON} className="btn btn-export">
            Export JSON
          </button>
          <button onClick={exportToCSV} className="btn btn-export">
            Export CSV
          </button>
          <button onClick={onReset} className="btn btn-reset">
            New Analysis
          </button>
        </div>
      </div>

      {results.results.length === 0 ? (
        <div className="no-results">
          <h3>No Known Errors Found</h3>
          <p>The log file was scanned but no matching error patterns were detected.</p>
        </div>
      ) : (
        <div className="results-list">
          {results.results.map((result, index) => (
            <div key={index} className="result-item">
              <div className="result-header" onClick={() => toggleExpand(index)}>
                <div className="result-number">#{index + 1}</div>
                <div className="result-info">
                  <div className="result-line-num">Line {result.line_number}</div>
                  <div className="result-interpretation">{result.interpretation}</div>
                </div>
                <div className={`expand-icon ${expandedIndex === index ? 'expanded' : ''}`}>
                  ▼
                </div>
              </div>

              {expandedIndex === index && (
                <div className="result-details">
                  <div className="detail-section">
                    <h4>Log Line:</h4>
                    <pre className="log-line-content">{result.log_line}</pre>
                  </div>
                  <div className="detail-section">
                    <h4>Interpretation:</h4>
                    <p className="interpretation-content">{result.interpretation}</p>
                  </div>
                  <div className="detail-section">
                    <h4>Location:</h4>
                    <p className="location-content">Line {result.line_number} in {results.log_filename}</p>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {results.total_errors > results.displayed_errors && (
        <div className="results-footer">
          <p>
            Showing {results.displayed_errors} of {results.total_errors} errors.
            To see all errors, remove the maximum errors limit and analyze again.
          </p>
        </div>
      )}
    </div>
  );
};

export default ResultsDisplay;
