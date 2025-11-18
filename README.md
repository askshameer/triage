# Platform Issue Triage Tool

A comprehensive solution for scanning log files and identifying known errors with both CLI and Web Dashboard interfaces.

## Features

- **Command-Line Interface (CLI)**: Original Python-based tool for terminal usage
- **Web Dashboard**: Modern TypeScript/React frontend with Flask backend API
- **File Upload**: Upload log files and custom error mapping Excel files
- **Flexible Configuration**: Limit results, use custom error mappings
- **Export Options**: Download results as JSON or CSV
- **Real-time Analysis**: Fast log file scanning and pattern matching

## Architecture

```
CheckPoint/
├── triage_tool.py         # Core CLI tool (original functionality)
├── app.py                 # Flask API backend
├── requirements.txt       # Python dependencies
├── error_mappings.xlsx    # Default error mappings (create this)
└── frontend/              # TypeScript/React web UI
    ├── src/
    │   ├── App.tsx
    │   ├── components/
    │   │   ├── UploadForm.tsx
    │   │   └── ResultsDisplay.tsx
    │   └── main.tsx
    └── package.json
```

## Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn

## Installation

### 1. Clone and Setup Python Backend

```bash
cd CheckPoint

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Create Error Mappings File

Create an `error_mappings.xlsx` file with at least 2 columns:
- **Column 1**: Error text to search for
- **Column 2**: Interpretation/description of the error

Example:
| Error Text | Interpretation |
|------------|----------------|
| Connection timeout | Network connectivity issue |
| Out of memory | Memory allocation failure |

### 3. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Build for production
npm run build
```

## Usage

### Option 1: Command-Line Interface (Original Tool)

The original CLI tool remains fully functional:

```bash
# Basic usage
python triage_tool.py -l /path/to/logfile.log

# Limit displayed errors
python triage_tool.py -l logfile.log -e 5

# Use custom error mappings
python triage_tool.py -l /var/log/app.log --excel custom_errors.xlsx -e 3
```

**CLI Options:**
- `-l, --logfile`: Path to log file (required)
- `-e, --errors`: Maximum number of errors to display
- `--excel`: Custom Excel file with error mappings (default: error_mappings.xlsx)
- `--version`: Show version information

### Option 2: Web Dashboard

#### Development Mode

Terminal 1 - Start Backend:
```bash
python app.py
```

Terminal 2 - Start Frontend:
```bash
cd frontend
npm run dev
```

Access the dashboard at: `http://localhost:3000`

#### Production Deployment

1. **Build Frontend:**
```bash
cd frontend
npm run build
```

2. **Serve Application:**

For production, you can:

**Option A: Use a production WSGI server (Recommended)**

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Option B: Serve frontend separately**

Use nginx or Apache to serve the `frontend/dist` folder and proxy API requests to the Flask backend.

Example nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/CheckPoint/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Web Dashboard Features

### Upload Form
- **Log File Upload**: Support for .log, .txt, .out files
- **Error Mappings**: Use default or upload custom Excel file
- **Max Errors Limit**: Control number of results displayed

### Results Display
- **Summary Statistics**: Total errors, mappings loaded, file info
- **Expandable Results**: Click to view detailed information
- **Export Options**: Download as JSON or CSV
- **Responsive Design**: Works on desktop, tablet, and mobile

## API Endpoints

### `GET /api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0"
}
```

### `POST /api/triage`
Perform log file triage analysis.

**Form Data:**
- `logfile` (required): Log file to analyze
- `excel_file` (optional): Custom error mappings Excel file
- `max_errors` (optional): Maximum number of errors to return

**Response:**
```json
{
  "total_errors": 10,
  "displayed_errors": 10,
  "log_filename": "app.log",
  "mappings_count": 25,
  "results": [
    {
      "line_number": 42,
      "log_line": "Error: Connection timeout",
      "interpretation": "Network connectivity issue"
    }
  ]
}
```

### `POST /api/validate-excel`
Validate Excel error mappings file.

**Form Data:**
- `excel_file` (required): Excel file to validate

**Response:**
```json
{
  "valid": true,
  "mappings_count": 25,
  "filename": "error_mappings.xlsx"
}
```

## Deployment for Demo

### Quick Deploy with Heroku

1. **Create `Procfile`:**
```
web: gunicorn app:app
```

2. **Deploy:**
```bash
heroku create your-app-name
git add .
git commit -m "Initial deployment"
git push heroku main
```

### Deploy with Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application
COPY triage_tool.py app.py ./
COPY error_mappings.xlsx .
COPY frontend/dist ./frontend/dist

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t triage-tool .
docker run -p 5000:5000 triage-tool
```

### Deploy to Cloud Platforms

#### AWS (Elastic Beanstalk, EC2, or Lambda)
#### Azure (App Service or Container Instances)
#### Google Cloud (App Engine or Cloud Run)

All major cloud platforms support Python Flask applications. Refer to their documentation for specific deployment steps.

## File Size Limits

- Maximum upload size: 100MB (configurable in `app.py`)
- Supported log formats: .log, .txt, .out
- Supported Excel formats: .xlsx, .xls

## Security Considerations

- Files are temporarily stored and immediately deleted after processing
- All uploads are validated for file type and size
- CORS is enabled for API access (configure appropriately for production)
- Secure filename handling with Werkzeug

## Troubleshooting

### "Excel file not found"
Ensure `error_mappings.xlsx` exists in the root directory or upload a custom file via the web dashboard.

### Frontend can't connect to backend
Check that the Flask backend is running on port 5000 and the proxy configuration in `vite.config.ts` is correct.

### Port already in use
Change the port in `app.py` (backend) or `vite.config.ts` (frontend).

## Development

### Backend Development
```bash
# Run with auto-reload
python app.py
```

### Frontend Development
```bash
cd frontend
npm run dev
```

The frontend will proxy API requests to `http://localhost:5000`.

## Technology Stack

### Backend
- Flask - Web framework
- Flask-CORS - Cross-origin resource sharing
- Pandas - Excel file processing
- OpenPyXL - Excel file reading

### Frontend
- React 18 - UI framework
- TypeScript - Type-safe JavaScript
- Vite - Build tool and dev server
- Axios - HTTP client

## License

This is a proprietary tool. All rights reserved.

## Version

v1.0 - Initial release with CLI and Web Dashboard
