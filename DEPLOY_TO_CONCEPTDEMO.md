# Deploy to www.conceptdemo.in - Quick Guide

Simple steps to deploy your Triage Tool to your Hostinger account at conceptdemo.in

## 🎯 Recommended Approach: Hybrid Deployment (Easiest)

Since Hostinger shared hosting may have Python limitations, the **easiest and free** solution is:

1. Deploy the app to **Render** (free cloud platform)
2. Point a subdomain from your Hostinger domain to it

### Why This Works Best:
- ✅ **Free** - No hosting costs for the app
- ✅ **Easy** - No Python/server configuration needed
- ✅ **Professional** - Use your own domain (triage.conceptdemo.in)
- ✅ **Automatic updates** - Deploy by pushing to Git
- ✅ **Always on** - App stays running (with slight delay on first request)

---

## 🚀 Quick Deploy (15 Minutes Total)

### Part 1: Deploy App to Render (10 min)

#### Step 1: Push to GitHub
```bash
cd /home/sameer/CheckPoint
git init
git add .
git commit -m "Deploy triage tool"

# Create repo on github.com first, then:
git remote add origin https://github.com/YOUR_USERNAME/triage-tool.git
git push -u origin main
```

#### Step 2: Deploy to Render
1. Go to [render.com](https://render.com) - Sign up with GitHub
2. Click **"New +"** → **"Web Service"**
3. Connect your repository
4. Settings:
   - **Name**: `conceptdemo-triage`
   - **Build Command**:
     ```
     cd frontend && npm install && npm run build && cd .. && pip install -r requirements.txt
     ```
   - **Start Command**:
     ```
     gunicorn --bind 0.0.0.0:$PORT app:app
     ```
   - **Plan**: Free

5. Click **"Create Web Service"**
6. Wait 5-10 minutes
7. You'll get URL like: `https://conceptdemo-triage.onrender.com`

### Part 2: Connect Your Domain (5 min)

#### Step 3: Create Subdomain in Hostinger
1. Login to **Hostinger hPanel** (https://hpanel.hostinger.com)
2. Go to **Domains** → **DNS / Name Servers**
3. Find your domain: **conceptdemo.in**
4. Click **"Manage"** or **"DNS Records"**

#### Step 4: Add DNS Record
Add a new CNAME record:
```
Type: CNAME
Name: triage
Target: conceptdemo-triage.onrender.com
TTL: 14400 (or Auto)
```

Click **"Save"** or **"Add Record"**

#### Step 5: Add Custom Domain in Render
1. Back in Render Dashboard → Your Service
2. Go to **"Settings"** tab
3. Scroll to **"Custom Domains"**
4. Click **"Add Custom Domain"**
5. Enter: `triage.conceptdemo.in`
6. Click **"Add"**
7. Wait 5-15 minutes for SSL to activate

### ✅ Done!

Your app is now live at:
- **https://triage.conceptdemo.in** (your custom domain)
- **https://conceptdemo-triage.onrender.com** (Render URL)

---

## 🔄 Alternative: Full Hostinger Deployment (VPS Only)

If you have Hostinger **VPS** or **Cloud Hosting** (not shared):

### Step 1: Get SSH Access

From Hostinger hPanel:
1. Go to **VPS** → **SSH Access**
2. Note down:
   - SSH Username
   - Server IP
   - SSH Password or setup SSH key

### Step 2: Configure Deployment Script

Edit `deploy_to_hostinger.sh`:
```bash
SSH_USER="your-username"        # Replace with your SSH username
SSH_HOST="your-vps-ip"          # Replace with your server IP
REMOTE_DIR="~/conceptdemo"      # Where to deploy
```

### Step 3: Run Deployment
```bash
cd /home/sameer/CheckPoint
./deploy_to_hostinger.sh
```

### Step 4: Configure Domain in Hostinger
1. hPanel → **Domains** → **conceptdemo.in**
2. Point to your VPS IP
3. Enable SSL in hPanel

See [HOSTINGER_DEPLOYMENT.md](HOSTINGER_DEPLOYMENT.md) for detailed VPS instructions.

---

## 📊 Comparison

| Method | Cost | Difficulty | Best For |
|--------|------|------------|----------|
| **Hybrid (Recommended)** | Free | Easy ⭐ | Shared hosting, demos |
| **Full Hostinger VPS** | VPS cost | Medium | Full control needed |
| **Direct Shared Hosting** | Included | Hard | Not recommended |

---

## 🧪 Test Your Deployment

After deployment, test these:

1. **Access URL**: https://triage.conceptdemo.in
2. **Upload log file** - Try with a .log or .txt file
3. **Upload Excel** - Test custom error mappings
4. **Check results** - Verify analysis works
5. **Export** - Download as JSON and CSV
6. **New checkboxes** - Click "Historical check" and "Advanced Triage (AI)"

---

## 🔐 Enable HTTPS

### For Hybrid Approach:
- Render provides HTTPS automatically
- DNS propagation may take 5-60 minutes

### For Hostinger VPS:
1. hPanel → **SSL**
2. Click **"Install"** for conceptdemo.in
3. Choose **"Let's Encrypt"** (Free)
4. Wait for activation

---

## 📱 Share Your App

Once deployed, you can share:
- **Main URL**: https://triage.conceptdemo.in
- **Description**: "Upload log files to automatically identify and analyze errors"

---

## 🐛 Troubleshooting

### DNS Not Working
- Wait up to 48 hours for DNS propagation (usually 5-15 min)
- Clear browser cache
- Try incognito mode
- Check DNS with: `nslookup triage.conceptdemo.in`

### "Site Can't Be Reached"
- Verify CNAME record in Hostinger
- Check Render app is running (green status)
- Wait for DNS propagation

### Upload Not Working
- Check file size (must be under 100MB)
- Verify file extension (.log, .txt, .out for logs)
- Check browser console for errors

### App Is Slow
- Free tier sleeps after 15 min inactivity
- First request after sleep takes ~30 seconds
- Subsequent requests are fast

---

## 🔄 Update Your App

To deploy changes:

### For Hybrid Approach:
```bash
git add .
git commit -m "Update description"
git push origin main
# Render auto-deploys in ~5 minutes
```

### For VPS:
```bash
./deploy_to_hostinger.sh
```

---

## 💡 Pro Tips

1. **Use Subdomain**: Keep main site at www.conceptdemo.in, app at triage.conceptdemo.in
2. **Bookmark Render Dashboard**: Easy access to logs and settings
3. **Monitor Usage**: Free tier has limits, monitor in Render dashboard
4. **Backup**: Keep GitHub repo updated as backup

---

## 📞 Support

- **Render Issues**: render.com documentation or support
- **Hostinger Issues**: Hostinger 24/7 support chat
- **App Issues**: Check [README.md](README.md) and [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## ✅ Deployment Checklist

**Hybrid Approach (Recommended):**
- [ ] Push code to GitHub
- [ ] Deploy to Render
- [ ] Add CNAME in Hostinger DNS
- [ ] Add custom domain in Render
- [ ] Wait for SSL activation
- [ ] Test the app
- [ ] Share the URL!

**VPS Approach:**
- [ ] Get SSH credentials from Hostinger
- [ ] Edit deploy_to_hostinger.sh
- [ ] Run deployment script
- [ ] Configure DNS
- [ ] Enable SSL
- [ ] Test the app

---

## 🎉 You're Ready!

**Recommended next step**: Use the **Hybrid Approach** above - it's the fastest and easiest!

Your app will be live at **https://triage.conceptdemo.in** in about 15 minutes.

Good luck! 🚀
