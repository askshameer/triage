#!/bin/bash

# Deployment script for Hostinger
# Configure the variables below before running

# ============================================
# CONFIGURATION - UPDATE THESE VALUES
# ============================================

# Your Hostinger SSH details
SSH_USER="your-username"           # Your Hostinger SSH username
SSH_HOST="your-server-ip"          # Your Hostinger server IP or hostname
REMOTE_DIR="~/public_html/triage"  # Remote directory path

# Or use subdomain directory
# REMOTE_DIR="~/domains/triage.conceptdemo.in/public_html"

# Local project path
LOCAL_DIR="/home/sameer/CheckPoint"

# ============================================
# DEPLOYMENT SCRIPT - NO NEED TO EDIT BELOW
# ============================================

echo "============================================"
echo "  Deploying to Hostinger - conceptdemo.in"
echo "============================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if configuration is set
if [ "$SSH_USER" = "your-username" ] || [ "$SSH_HOST" = "your-server-ip" ]; then
    echo -e "${RED}ERROR: Please configure SSH_USER and SSH_HOST in this script${NC}"
    echo "Edit deploy_to_hostinger.sh and update the configuration section"
    exit 1
fi

# Step 1: Build Frontend
echo -e "${YELLOW}Step 1: Building frontend...${NC}"
cd "$LOCAL_DIR/frontend" || exit 1

if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

npm run build
if [ $? -ne 0 ]; then
    echo -e "${RED}Frontend build failed!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Frontend built successfully${NC}"
echo ""

# Step 2: Create deployment package
echo -e "${YELLOW}Step 2: Creating deployment package...${NC}"
cd "$LOCAL_DIR" || exit 1

# Create temporary directory for deployment files
TEMP_DIR=$(mktemp -d)
echo "Using temp directory: $TEMP_DIR"

# Copy necessary files
cp app.py "$TEMP_DIR/"
cp triage_tool.py "$TEMP_DIR/"
cp requirements.txt "$TEMP_DIR/"
cp passenger_wsgi.py "$TEMP_DIR/"
cp .htaccess "$TEMP_DIR/"

# Copy error mappings if exists
if [ -f "error_mappings.xlsx" ]; then
    cp error_mappings.xlsx "$TEMP_DIR/"
    echo "✓ Copied error_mappings.xlsx"
fi

# Copy built frontend
mkdir -p "$TEMP_DIR/frontend"
cp -r frontend/dist "$TEMP_DIR/frontend/"

echo -e "${GREEN}✓ Deployment package ready${NC}"
echo ""

# Step 3: Upload to Hostinger
echo -e "${YELLOW}Step 3: Uploading files to Hostinger...${NC}"
echo "Connecting to: $SSH_USER@$SSH_HOST"

# Create remote directory
ssh "$SSH_USER@$SSH_HOST" "mkdir -p $REMOTE_DIR"

# Upload files
rsync -avz --progress \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='venv' \
    "$TEMP_DIR/" "$SSH_USER@$SSH_HOST:$REMOTE_DIR/"

if [ $? -ne 0 ]; then
    echo -e "${RED}Upload failed!${NC}"
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo -e "${GREEN}✓ Files uploaded successfully${NC}"
echo ""

# Clean up temp directory
rm -rf "$TEMP_DIR"

# Step 4: Setup on server
echo -e "${YELLOW}Step 4: Setting up environment on server...${NC}"

ssh "$SSH_USER@$SSH_HOST" bash << ENDSSH
    cd $REMOTE_DIR

    echo "Creating virtual environment..."
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi

    echo "Activating virtual environment..."
    source venv/bin/activate

    echo "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt

    echo "Setting permissions..."
    chmod -R 755 .
    chmod 644 *.py
    chmod 644 passenger_wsgi.py

    echo ""
    echo "✓ Server setup complete"

    # Update .htaccess with correct path
    FULL_PATH=\$(pwd)
    sed -i "s|/home/your-username/conceptdemo|\$FULL_PATH|g" .htaccess

    echo "✓ Configuration updated"
ENDSSH

if [ $? -ne 0 ]; then
    echo -e "${RED}Server setup failed!${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Server setup complete${NC}"
echo ""

# Step 5: Final instructions
echo "============================================"
echo -e "${GREEN}  Deployment Complete! 🎉${NC}"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Configure your domain in Hostinger hPanel:"
echo "   - Point domain/subdomain to: $REMOTE_DIR"
echo "   - Enable SSL certificate"
echo ""
echo "2. Access your application:"
echo "   https://www.conceptdemo.in"
echo "   or"
echo "   https://triage.conceptdemo.in (if using subdomain)"
echo ""
echo "3. Check logs if needed:"
echo "   ssh $SSH_USER@$SSH_HOST 'tail -f $REMOTE_DIR/error.log'"
echo ""
echo "4. Restart application:"
echo "   ssh $SSH_USER@$SSH_HOST 'touch $REMOTE_DIR/tmp/restart.txt'"
echo ""
echo "============================================"
