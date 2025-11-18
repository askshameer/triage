# Deploy to Hostinger - www.conceptdemo.in

Complete guide to deploy your Platform Issue Triage Tool to Hostinger.

## 📋 Prerequisites

- ✅ Hostinger hosting account (you have this)
- ✅ Domain: www.conceptdemo.in (you have this)
- ✅ SSH/FTP access to Hostinger
- ✅ Python support on your hosting plan

---

## 🔍 Step 0: Check Your Hostinger Plan

Hostinger offers different plans with different capabilities:

1. **Shared Hosting** - May have limited Python support
2. **VPS Hosting** - Full Python/Node.js support (recommended)
3. **Cloud Hosting** - Full support

**Check your plan:**
- Login to Hostinger hPanel
- Check if you have SSH access
- Check if Python/Node.js is available

---

## 🚀 Deployment Method

### Method 1: VPS/Cloud Hosting (Full Control) - RECOMMENDED

If you have VPS or Cloud hosting:

#### Step 1: Build Frontend Locally

```bash
cd /home/sameer/CheckPoint/frontend
npm install
npm run build
cd ..
```

#### Step 2: Connect to Hostinger via SSH

```bash
# Get SSH credentials from Hostinger hPanel
ssh username@your-server-ip
```

#### Step 3: Setup on Server

```bash
# Create directory for your app
mkdir -p ~/conceptdemo
cd ~/conceptdemo

# Upload files (we'll do this next)
```

#### Step 4: Upload Files

**Option A: Using SCP (from your local machine)**
```bash
cd /home/sameer/CheckPoint

# Upload all files
scp -r app.py triage_tool.py requirements.txt frontend/dist username@your-server-ip:~/conceptdemo/
scp -r error_mappings.xlsx username@your-server-ip:~/conceptdemo/ # if you have it
```

**Option B: Using Git (recommended)**
```bash
# On your server (via SSH)
cd ~/conceptdemo
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git .

# Build frontend on server
cd frontend
npm install
npm run build
cd ..
```

#### Step 5: Install Dependencies on Server

```bash
# On Hostinger server via SSH
cd ~/conceptdemo

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

#### Step 6: Configure Web Server

**For Apache (most common on Hostinger):**

Create `.htaccess` file in your domain's public_html:
```apache
# Redirect all traffic to Python app
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ http://localhost:5000/$1 [P,L]
```

**Or use a subdomain** like `triage.conceptdemo.in`:
- Create subdomain in hPanel
- Point it to your app directory
- Configure reverse proxy

#### Step 7: Run the Application

```bash
# Start with gunicorn (production server)
cd ~/conceptdemo
source venv/bin/activate
gunicorn --bind 0.0.0.0:5000 --daemon app:app

# Or use nohup to keep it running
nohup gunicorn --bind 0.0.0.0:5000 app:app > app.log 2>&1 &
```

#### Step 8: Setup as a Service (Keep Running)

Create systemd service file: `/etc/systemd/system/triage-tool.service`

```ini
[Unit]
Description=Platform Triage Tool
After=network.target

[Service]
User=your-username
WorkingDirectory=/home/your-username/conceptdemo
Environment="PATH=/home/your-username/conceptdemo/venv/bin"
ExecStart=/home/your-username/conceptdemo/venv/bin/gunicorn --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable triage-tool
sudo systemctl start triage-tool
sudo systemctl status triage-tool
```

---

### Method 2: Shared Hosting (Limited Python Support)

If you have shared hosting with limited Python support, you have these options:

#### Option A: Use Subdomain with Reverse Proxy

1. Create a subdomain in Hostinger hPanel (e.g., `triage.conceptdemo.in`)
2. Deploy to a cloud platform (Render/Heroku) - FREE
3. Use Hostinger's reverse proxy to redirect subdomain to cloud platform
4. Main domain stays on Hostinger, app runs on cloud

**Steps:**
```bash
# Deploy to Render (free) as per QUICK_START.md
# Get the URL: https://your-app.onrender.com

# In Hostinger, create CNAME record:
# Name: triage
# Target: your-app.onrender.com
```

#### Option B: Static Frontend + Cloud Backend

1. Upload built frontend to Hostinger
2. Backend runs on free cloud service
3. Frontend makes API calls to backend

---

## 📁 Files to Upload to Hostinger

### Essential Files:
```
conceptdemo/
├── app.py                    # Flask backend
├── triage_tool.py            # Core logic
├── requirements.txt          # Python dependencies
├── error_mappings.xlsx       # Error mappings (optional)
├── frontend/
│   └── dist/                 # Built frontend
│       ├── index.html
│       └── assets/
├── venv/                     # Virtual environment (create on server)
└── passenger_wsgi.py         # WSGI config (if using Passenger)
```

### Don't Upload:
- `node_modules/` (too large)
- `venv/` or `.venv/` (create on server)
- `__pycache__/`
- `.git/` (unless using git clone)

---

## 🔧 Create WSGI Configuration

For Passenger (common on shared hosting), create `passenger_wsgi.py`:

```python
import sys
import os

# Add your application directory to the Python path
INTERP = os.path.join(os.environ['HOME'], 'conceptdemo', 'venv', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Set the working directory
sys.path.insert(0, os.path.join(os.environ['HOME'], 'conceptdemo'))

# Import the Flask app
from app import app as application
```

---

## 🌐 DNS Configuration for conceptdemo.in

### Option 1: Main Domain Points to App

In Hostinger DNS settings:
```
A Record:
Name: @
Points to: Your server IP
TTL: 14400

A Record:
Name: www
Points to: Your server IP
TTL: 14400
```

### Option 2: Subdomain for App (Recommended)

```
A Record:
Name: triage
Points to: Your server IP
TTL: 14400
```

Access at: `https://triage.conceptdemo.in`

---

## 🔐 SSL Certificate (HTTPS)

### Enable SSL in Hostinger:

1. Go to Hostinger hPanel
2. Navigate to SSL section
3. Enable free Let's Encrypt SSL for your domain/subdomain
4. Wait 15 minutes for activation

Your app will be accessible via HTTPS automatically.

---

## 📦 Quick Deployment Script for Hostinger

Save this as `deploy_to_hostinger.sh`:

```bash
#!/bin/bash

# Configuration
SERVER="username@your-server-ip"
REMOTE_DIR="~/conceptdemo"
LOCAL_DIR="/home/sameer/CheckPoint"

echo "Building frontend..."
cd $LOCAL_DIR/frontend
npm install
npm run build

echo "Uploading files to Hostinger..."
cd $LOCAL_DIR

# Upload files via SCP
scp app.py triage_tool.py requirements.txt $SERVER:$REMOTE_DIR/
scp -r frontend/dist $SERVER:$REMOTE_DIR/frontend/

# Optional: upload error mappings
if [ -f error_mappings.xlsx ]; then
    scp error_mappings.xlsx $SERVER:$REMOTE_DIR/
fi

echo "Installing dependencies on server..."
ssh $SERVER << 'ENDSSH'
cd ~/conceptdemo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "Deployment complete!"
ENDSSH

echo "Restarting application..."
ssh $SERVER "cd ~/conceptdemo && pkill gunicorn; nohup venv/bin/gunicorn --bind 0.0.0.0:5000 app:app > app.log 2>&1 &"

echo "✅ Deployment to Hostinger complete!"
echo "Your app should be running at https://www.conceptdemo.in"
```

Make it executable:
```bash
chmod +x deploy_to_hostinger.sh
```

---

## 🧪 Testing Your Deployment

After deployment, test:

1. **Access the URL**: `https://www.conceptdemo.in` or `https://triage.conceptdemo.in`
2. **Upload a log file**
3. **Check if analysis works**
4. **Test export functionality**
5. **Test new checkboxes** (should show popup)

---

## 🐛 Troubleshooting

### Can't Connect via SSH
- Check SSH credentials in Hostinger hPanel
- Verify SSH is enabled for your plan
- Try using Hostinger's built-in SSH browser terminal

### Python Version Issues
```bash
# Check Python version on server
python3 --version

# If too old, check for alternatives
python3.11 --version
python3.10 --version
```

### Permission Denied
```bash
# Fix permissions
chmod -R 755 ~/conceptdemo
```

### Port Already in Use
```bash
# Find and kill process using port 5000
lsof -ti:5000 | xargs kill -9

# Or use a different port
gunicorn --bind 0.0.0.0:5001 app:app
```

### App Not Accessible from Outside
- Configure firewall to allow port 5000
- Set up reverse proxy (Apache/Nginx)
- Use Hostinger's built-in app deployment tools

### Frontend Not Loading
```bash
# Verify frontend files exist
ls -la ~/conceptdemo/frontend/dist/

# Check Flask static folder config in app.py
```

---

## 📊 Hostinger-Specific Features

### File Manager
- Use Hostinger's file manager in hPanel
- Upload files directly through browser
- Extract ZIP files on server

### Databases
- If you need database later, create MySQL in hPanel
- Update app.py to use database

### Cron Jobs
- Set up in hPanel for scheduled tasks
- Useful for log cleanup, etc.

---

## 🔄 Updating Your App

To update after making changes:

```bash
# Local: rebuild frontend
cd /home/sameer/CheckPoint/frontend
npm run build

# Upload changes
./deploy_to_hostinger.sh

# Or manually:
scp -r frontend/dist username@server:~/conceptdemo/frontend/
scp app.py username@server:~/conceptdemo/

# Restart app
ssh username@server "pkill gunicorn; cd ~/conceptdemo && nohup venv/bin/gunicorn --bind 0.0.0.0:5000 app:app > app.log 2>&1 &"
```

---

## 💡 Recommended Setup for www.conceptdemo.in

### Best Approach:

1. **Subdomain Strategy**:
   - Main site: `www.conceptdemo.in` (your main content)
   - Triage app: `triage.conceptdemo.in` (this application)

2. **Hybrid Approach** (if Python support is limited):
   - Deploy to Render (free): Get `https://your-app.onrender.com`
   - Create CNAME: `triage.conceptdemo.in` → `your-app.onrender.com`
   - Benefits: Free, easy, always updated

3. **Full VPS Approach** (if you have VPS):
   - Deploy directly on Hostinger VPS
   - Full control, no external dependencies

---

## 📞 Need Help?

1. **Check Hostinger Documentation**: hPanel → Help
2. **Contact Hostinger Support**: 24/7 support available
3. **Check Server Logs**: `~/conceptdemo/app.log`
4. **Test Locally First**: `./deploy_local.sh`

---

## ✅ Deployment Checklist

- [ ] Determine hosting type (Shared/VPS/Cloud)
- [ ] Get SSH credentials from Hostinger hPanel
- [ ] Build frontend locally (`npm run build`)
- [ ] Upload files to Hostinger
- [ ] Install Python dependencies on server
- [ ] Configure web server (Apache/Nginx)
- [ ] Set up SSL certificate
- [ ] Test the application
- [ ] Set up automatic restart (systemd/supervisor)
- [ ] Configure DNS (if using subdomain)

---

**Choose the method that fits your Hostinger plan and follow the steps above!**

**For fastest results**: Use the hybrid approach (deploy to Render + CNAME to your domain).
