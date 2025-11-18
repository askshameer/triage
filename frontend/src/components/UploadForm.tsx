import React, { useState } from 'react';
import axios from 'axios';
import { TriageResponse } from '../App';
import './UploadForm.css';

interface UploadFormProps {
  onTriageComplete: (data: TriageResponse) => void;
  onError: (error: string) => void;
  onLoadingChange: (loading: boolean) => void;
  onReset: () => void;
}

const UploadForm: React.FC<UploadFormProps> = ({
  onTriageComplete,
  onError,
  onLoadingChange,
  onReset
}) => {
  const [logFile, setLogFile] = useState<File | null>(null);
  const [excelFile, setExcelFile] = useState<File | null>(null);
  const [maxErrors, setMaxErrors] = useState<string>('');
  const [useDefaultExcel, setUseDefaultExcel] = useState(true);
  const [historicalCheck, setHistoricalCheck] = useState(false);
  const [advancedTriage, setAdvancedTriage] = useState(false);

  const handleLogFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setLogFile(e.target.files[0]);
      onReset();
    }
  };

  const handleExcelFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setExcelFile(e.target.files[0]);
      onReset();
    }
  };

  const handleMaxErrorsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (value === '' || /^\d+$/.test(value)) {
      setMaxErrors(value);
    }
  };

  const handleFeatureCheckbox = () => {
    alert('Feature not implemented');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!logFile) {
      onError('Please select a log file to analyze');
      return;
    }

    if (!useDefaultExcel && !excelFile) {
      onError('Please select an Excel file or use the default error mappings');
      return;
    }

    const formData = new FormData();
    formData.append('logfile', logFile);

    if (!useDefaultExcel && excelFile) {
      formData.append('excel_file', excelFile);
    }

    if (maxErrors !== '') {
      const maxErrorsNum = parseInt(maxErrors, 10);
      if (maxErrorsNum < 1) {
        onError('Maximum errors must be at least 1');
        return;
      }
      formData.append('max_errors', maxErrors);
    }

    try {
      onLoadingChange(true);
      onError('');

      const response = await axios.post<TriageResponse>('/api/triage', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      onTriageComplete(response.data);
    } catch (err: any) {
      if (err.response && err.response.data && err.response.data.error) {
        onError(err.response.data.error);
      } else {
        onError('Failed to analyze log file. Please try again.');
      }
    } finally {
      onLoadingChange(false);
    }
  };

  const handleReset = () => {
    setLogFile(null);
    setExcelFile(null);
    setMaxErrors('');
    setUseDefaultExcel(true);
    setHistoricalCheck(false);
    setAdvancedTriage(false);
    onReset();

    // Reset file inputs
    const logInput = document.getElementById('logfile-input') as HTMLInputElement;
    const excelInput = document.getElementById('excelfile-input') as HTMLInputElement;
    if (logInput) logInput.value = '';
    if (excelInput) excelInput.value = '';
  };

  return (
    <div className="upload-form-container">
      <form onSubmit={handleSubmit} className="upload-form">
        <div className="form-section">
          <h2>Log File</h2>
          <div className="form-group">
            <label htmlFor="logfile-input">
              Select Log File <span className="required">*</span>
            </label>
            <input
              id="logfile-input"
              type="file"
              accept=".log,.txt,.out"
              onChange={handleLogFileChange}
              className="file-input"
            />
            {logFile && (
              <div className="file-info">
                Selected: {logFile.name} ({(logFile.size / 1024).toFixed(2)} KB)
              </div>
            )}
          </div>
        </div>

        <div className="form-section">
          <h2>Analysis Options</h2>
          <div className="form-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={useDefaultExcel}
                onChange={(e) => setUseDefaultExcel(e.target.checked)}
              />
              <span>Use Checkpoint (default error_mappings.xlsx)</span>
            </label>
          </div>

          <div className="form-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={historicalCheck}
                onChange={() => {
                  handleFeatureCheckbox();
                }}
              />
              <span>Historical check</span>
            </label>
          </div>

          <div className="form-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={advancedTriage}
                onChange={() => {
                  handleFeatureCheckbox();
                }}
              />
              <span>Advanced Triage (AI)</span>
            </label>
          </div>

          {!useDefaultExcel && (
            <div className="form-group">
              <label htmlFor="excelfile-input">
                Custom Excel File <span className="required">*</span>
              </label>
              <input
                id="excelfile-input"
                type="file"
                accept=".xlsx,.xls"
                onChange={handleExcelFileChange}
                className="file-input"
              />
              {excelFile && (
                <div className="file-info">
                  Selected: {excelFile.name} ({(excelFile.size / 1024).toFixed(2)} KB)
                </div>
              )}
            </div>
          )}
        </div>

        <div className="form-section">
          <h2>Options</h2>
          <div className="form-group">
            <label htmlFor="max-errors-input">
              Maximum Errors to Display (optional)
            </label>
            <input
              id="max-errors-input"
              type="text"
              value={maxErrors}
              onChange={handleMaxErrorsChange}
              placeholder="Leave empty to show all errors"
              className="text-input"
            />
            <div className="help-text">
              Limit the number of errors shown in results. Leave empty to display all.
            </div>
          </div>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn btn-primary">
            Analyze Log File
          </button>
          <button type="button" onClick={handleReset} className="btn btn-secondary">
            Reset
          </button>
        </div>
      </form>
    </div>
  );
};

export default UploadForm;
