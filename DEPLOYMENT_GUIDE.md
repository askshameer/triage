# Deployment Guide - Platform Issue Triage Tool

This guide will help you publish your web application to various hosting platforms.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Start - Local Production Build](#quick-start---local-production-build)
3. [Deploy to Render (Recommended - FREE)](#deploy-to-render-recommended---free)
4. [Deploy to Heroku](#deploy-to-heroku)
5. [Deploy to Railway](#deploy-to-railway)
6. [Deploy with Docker](#deploy-with-docker)
7. [Deploy to AWS](#deploy-to-aws)
8. [Custom Domain Setup](#custom-domain-setup)

---

## Prerequisites

Before deploying, ensure you have:
- Git installed and repository initialized
- Python 3.11+ installed
- Node.js 18+ installed
- An `error_mappings.xlsx` file (or users will need to upload their own)

---

## Quick Start - Local Production Build

Test your production build locally before deploying:

### Step 1: Build the Frontend
```bash
cd frontend
npm install
npm run build
cd ..
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Production Server
```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

### Step 4: Test
Open browser to `http://localhost:5000`

---

## Deploy to Render (Recommended - FREE)

**Why Render?** Free tier, easy setup, automatic deployments from Git.

### Step-by-Step Instructions:

1. **Create a Git Repository** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit for deployment"
   ```

2. **Push to GitHub**:
   ```bash
   # Create a new repository on GitHub first
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git branch -M main
   git push -u origin main
   ```

3. **Deploy to Render**:
   - Go to [render.com](https://render.com)
   - Sign up/Login with GitHub
   - Click "New +" → "Web Service"
   - Connect your repository
   - Configure:
     - **Name**: `triage-tool` (or your preferred name)
     - **Environment**: `Python 3`
     - **Build Command**:
       ```bash
       cd frontend && npm install && npm run build && cd .. && pip install -r requirements.txt
       ```
     - **Start Command**:
       ```bash
       gunicorn --bind 0.0.0.0:$PORT app:app
       ```
     - **Plan**: Free

4. **Add Environment Variables** (if needed):
   - Click "Environment" tab
   - Add any custom configurations

5. **Deploy**:
   - Click "Create Web Service"
   - Wait 5-10 minutes for first deployment
   - Your app will be live at `https://your-app-name.onrender.com`

**Note**: Free tier sleeps after 15 minutes of inactivity. First request may take 30 seconds to wake up.

---

## Deploy to Heroku

**Why Heroku?** Well-established platform, easy to use.

### Step-by-Step Instructions:

1. **Install Heroku CLI**:
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku

   # Ubuntu
   curl https://cli-assets.heroku.com/install.sh | sh

   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**:
   ```bash
   heroku login
   ```

3. **Create Heroku App**:
   ```bash
   heroku create your-triage-tool-name
   ```

4. **Add Buildpacks**:
   ```bash
   heroku buildpacks:add --index 1 heroku/nodejs
   heroku buildpacks:add --index 2 heroku/python
   ```

5. **Create `package.json` in Root** (for Heroku to build frontend):
   ```bash
   cat > package.json << 'EOF'
   {
     "name": "triage-tool",
     "version": "1.0.0",
     "scripts": {
       "build": "cd frontend && npm install && npm run build",
       "heroku-postbuild": "npm run build"
     }
   }
   EOF
   ```

6. **Deploy**:
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

7. **Open Your App**:
   ```bash
   heroku open
   ```

**View logs**:
```bash
heroku logs --tail
```

---

## Deploy to Railway

**Why Railway?** Simple, modern, generous free tier.

### Step-by-Step Instructions:

1. **Go to [railway.app](https://railway.app)**
2. **Sign up/Login with GitHub**
3. **Click "New Project"** → "Deploy from GitHub repo"
4. **Select your repository**
5. **Railway auto-detects settings**, but verify:
   - Build Command: `cd frontend && npm install && npm run build && cd .. && pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT app:app`
6. **Add Environment Variables** (if needed)
7. **Deploy** - Railway automatically deploys
8. **Get Public URL**: Click "Settings" → "Generate Domain"

---

## Deploy with Docker

**Why Docker?** Works anywhere, consistent environments.

### Step-by-Step Instructions:

1. **Build Docker Image**:
   ```bash
   docker build -t triage-tool .
   ```

2. **Test Locally**:
   ```bash
   docker run -p 5000:5000 triage-tool
   ```
   Open `http://localhost:5000`

3. **Deploy to Cloud**:

   **Option A: Deploy to Docker Hub + Any Cloud**
   ```bash
   # Tag and push to Docker Hub
   docker tag triage-tool YOUR_DOCKERHUB_USERNAME/triage-tool
   docker push YOUR_DOCKERHUB_USERNAME/triage-tool
   ```

   **Option B: Deploy to Google Cloud Run**
   ```bash
   # Install gcloud CLI first
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/triage-tool
   gcloud run deploy triage-tool --image gcr.io/YOUR_PROJECT_ID/triage-tool --platform managed --region us-central1 --allow-unauthenticated
   ```

   **Option C: Deploy to AWS ECS**
   ```bash
   # Install AWS CLI and configure credentials
   aws ecr create-repository --repository-name triage-tool
   docker tag triage-tool:latest YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com/triage-tool:latest
   docker push YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com/triage-tool:latest
   # Then create ECS task and service via AWS Console
   ```

---

## Deploy to AWS

### Option 1: AWS Elastic Beanstalk (Easiest)

1. **Install EB CLI**:
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB**:
   ```bash
   eb init -p python-3.11 triage-tool
   ```

3. **Create Environment**:
   ```bash
   eb create triage-tool-env
   ```

4. **Deploy**:
   ```bash
   eb deploy
   ```

5. **Open**:
   ```bash
   eb open
   ```

### Option 2: AWS EC2 (Manual)

1. **Launch EC2 Instance** (Ubuntu 22.04)
2. **SSH into Instance**:
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Install Dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3-pip nodejs npm -y
   ```

4. **Clone Repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
   cd YOUR_REPO
   ```

5. **Build and Run**:
   ```bash
   cd frontend && npm install && npm run build && cd ..
   pip install -r requirements.txt
   gunicorn --bind 0.0.0.0:5000 app:app
   ```

6. **Setup as Service** (optional - keeps running):
   ```bash
   sudo nano /etc/systemd/system/triage-tool.service
   ```

   Add:
   ```ini
   [Unit]
   Description=Triage Tool Web App
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/YOUR_REPO
   ExecStart=/usr/local/bin/gunicorn --bind 0.0.0.0:5000 app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   sudo systemctl enable triage-tool
   sudo systemctl start triage-tool
   ```

7. **Configure Security Group** - Open port 5000

---

## Custom Domain Setup

Once deployed, you can add a custom domain:

### For Render:
1. Go to Dashboard → Settings → Custom Domains
2. Add your domain (e.g., `triage.yourdomain.com`)
3. Add CNAME record in your DNS provider:
   - Name: `triage`
   - Value: `your-app.onrender.com`

### For Heroku:
```bash
heroku domains:add triage.yourdomain.com
```
Then add DNS record as shown by Heroku.

### For Railway:
1. Settings → Domains → Custom Domain
2. Follow DNS instructions

---

## Post-Deployment Checklist

- [ ] Test file upload functionality
- [ ] Test with sample log file
- [ ] Test with custom Excel file
- [ ] Verify export (JSON/CSV) works
- [ ] Check mobile responsiveness
- [ ] Monitor error logs
- [ ] Set up monitoring (optional)
- [ ] Configure custom domain (optional)
- [ ] Set up HTTPS (most platforms do this automatically)

---

## Troubleshooting

### Build Fails
- Check Node.js version: `node --version` (should be 18+)
- Check Python version: `python --version` (should be 3.11+)
- Clear npm cache: `cd frontend && npm cache clean --force`

### App Crashes on Startup
- Check logs: `heroku logs --tail` or equivalent
- Verify all dependencies in `requirements.txt`
- Ensure `error_mappings.xlsx` exists or handle missing file

### File Upload Not Working
- Check file size limits (default 100MB)
- Verify write permissions to temp directory
- Check error logs for specific errors

### Frontend Not Loading
- Verify frontend was built: Check if `frontend/dist/` exists
- Check Flask static folder configuration in `app.py`
- Verify all routes are correctly configured

---

## Monitoring and Maintenance

### Check Application Health
```bash
curl https://your-app-url.com/api/health
```

### View Logs
- **Render**: Dashboard → Logs
- **Heroku**: `heroku logs --tail`
- **Railway**: Dashboard → Deployments → View Logs
- **AWS**: CloudWatch Logs

### Update Application
```bash
git add .
git commit -m "Update description"
git push origin main  # Auto-deploys on Render/Railway
# OR
git push heroku main  # For Heroku
```

---

## Cost Estimates

| Platform | Free Tier | Paid Plans |
|----------|-----------|------------|
| Render | 750 hours/month | $7/month |
| Heroku | 550 hours/month (with credit card) | $7/month |
| Railway | $5 credit/month | Pay as you go |
| Google Cloud Run | 2 million requests/month | Pay per use |
| AWS Elastic Beanstalk | Free tier 1 year | ~$10-30/month |

---

## Need Help?

- Check [README.md](README.md) for application documentation
- Review platform-specific documentation
- Check application logs for errors
- Ensure all prerequisites are met

---

## Quick Deploy Commands Summary

### Render (Recommended)
```bash
git push origin main
# Deploy happens automatically
```

### Heroku
```bash
git push heroku main
```

### Railway
```bash
git push origin main
# Deploy happens automatically
```

### Docker
```bash
docker build -t triage-tool .
docker run -p 5000:5000 triage-tool
```

---

**Your application is now ready to be published! Choose the platform that best fits your needs and follow the instructions above.**
