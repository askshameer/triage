# Quick Start - Publish Your Webpage

Follow these simple steps to publish your Platform Issue Triage Tool web application.

## 🚀 Fastest Way: Deploy to Render (FREE)

**Total Time: ~10 minutes**

### Step 1: Prepare Your Code
```bash
cd /home/sameer/CheckPoint

# Initialize git if not done
git init
git add .
git commit -m "Ready for deployment"
```

### Step 2: Push to GitHub
1. Go to [github.com](https://github.com) and create a new repository
2. Push your code:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

### Step 3: Deploy on Render
1. Go to [render.com](https://render.com) and sign up (use your GitHub account)
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect GitHub"** and select your repository
4. Fill in the form:
   - **Name**: `triage-tool` (or any name you like)
   - **Environment**: `Python 3`
   - **Build Command**:
     ```
     cd frontend && npm install && npm run build && cd .. && pip install -r requirements.txt
     ```
   - **Start Command**:
     ```
     gunicorn --bind 0.0.0.0:$PORT app:app
     ```
   - **Instance Type**: `Free`

5. Click **"Create Web Service"**
6. Wait 5-10 minutes for deployment
7. Your app will be live at: `https://your-app-name.onrender.com` 🎉

**Note**: The free tier sleeps after inactivity, so the first request after idle time may take ~30 seconds.

---

## 💻 Test Locally First (Optional)

Before deploying, you can test the production build on your computer:

### Option 1: Use the Deploy Script
```bash
cd /home/sameer/CheckPoint
./deploy_local.sh
```

### Option 2: Manual Steps
```bash
# 1. Build frontend
cd frontend
npm install
npm run build
cd ..

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Run production server
gunicorn --bind 0.0.0.0:5000 app:app

# 4. Open browser to http://localhost:5000
```

---

## 🌐 Alternative Hosting Options

### Heroku (Easy, Established)
```bash
heroku create your-app-name
git push heroku main
heroku open
```
See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for details.

### Railway (Modern, Simple)
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Deploy from repo
4. Done!

### Docker (Universal)
```bash
docker build -t triage-tool .
docker run -p 5000:5000 triage-tool
```

---

## 📋 Pre-Deployment Checklist

- [ ] Create `error_mappings.xlsx` file (or users will upload their own)
- [ ] Test locally with `./deploy_local.sh`
- [ ] Create GitHub repository
- [ ] Choose hosting platform (Render recommended)
- [ ] Deploy!

---

## 📁 Important Files for Deployment

All deployment files are ready:
- ✅ `Procfile` - Heroku configuration
- ✅ `Dockerfile` - Docker configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `package.json` - Node.js build configuration
- ✅ `runtime.txt` - Python version
- ✅ `app.py` - Backend with static file serving
- ✅ `frontend/dist/` - Built frontend (after `npm run build`)

---

## 🔍 Verify Deployment

After deployment, test these features:
1. Upload a log file (.log, .txt, .out)
2. Upload a custom Excel file (optional)
3. Set max errors limit (optional)
4. Click "Analyze Log File"
5. View results
6. Export results (JSON/CSV)
7. Test new checkboxes (should show "Feature not implemented")

---

## 🆘 Need Help?

1. **Build fails?**
   - Check Node.js version: `node --version` (need 18+)
   - Check Python version: `python3 --version` (need 3.11+)

2. **App crashes?**
   - Check logs on your hosting platform
   - Verify `error_mappings.xlsx` exists or is optional

3. **More details?**
   - See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for comprehensive instructions
   - See [README.md](README.md) for application documentation

---

## 🎯 Recommended: Render Deployment

**Why Render?**
- ✅ Free tier (no credit card needed)
- ✅ Automatic deploys from GitHub
- ✅ HTTPS included
- ✅ Easy to use
- ✅ Good for demos and small projects

**Your URL will be**: `https://YOUR-APP-NAME.onrender.com`

---

## 🔗 Custom Domain (Optional)

After deployment, you can add your own domain:

1. In Render Dashboard → Settings → Custom Domains
2. Add your domain (e.g., `triage.yourdomain.com`)
3. Update your DNS with the CNAME record provided

---

**You're all set! Choose a platform and deploy your webpage now! 🚀**
