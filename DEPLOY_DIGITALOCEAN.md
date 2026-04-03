# Deploying Imani Fellowship AGC to DigitalOcean

A step-by-step guide to deploy this website on a DigitalOcean Droplet with PostgreSQL, Nginx, SSL, and DigitalOcean Spaces for file uploads.

**Estimated time:** 45–60 minutes  
**Cost:** ~$6/month (basic Droplet) + ~$5/month (Spaces) + domain cost

---

## Table of Contents

1. [Create a DigitalOcean Account](#1-create-a-digitalocean-account)
2. [Create a Droplet (Server)](#2-create-a-droplet-server)
3. [Connect to Your Server](#3-connect-to-your-server)
4. [Install System Dependencies](#4-install-system-dependencies)
5. [Set Up PostgreSQL Database](#5-set-up-postgresql-database)
6. [Deploy the Application](#6-deploy-the-application)
7. [Configure Gunicorn (App Server)](#7-configure-gunicorn-app-server)
8. [Configure Nginx (Web Server)](#8-configure-nginx-web-server)
9. [Set Up SSL/HTTPS (Free with Certbot)](#9-set-up-sslhttps-free-with-certbot)
10. [Set Up DigitalOcean Spaces (File Uploads)](#10-set-up-digitalocean-spaces-file-uploads)
11. [Point Your Domain](#11-point-your-domain)
12. [Update M-Pesa Callback URL](#12-update-m-pesa-callback-url)
13. [Create Admin User](#13-create-admin-user)
14. [Set Up Automated Backups](#14-set-up-automated-backups)
15. [Updating the Site](#15-updating-the-site)
16. [Troubleshooting](#16-troubleshooting)

---

## 1. Create a DigitalOcean Account

1. Go to [digitalocean.com](https://www.digitalocean.com/)
2. Click **Sign Up**
3. Create your account (you can use GitHub login)
4. Add a payment method (credit card or PayPal)
5. You may get $200 free credit for 60 days as a new user

---

## 2. Create a Droplet (Server)

1. From the DigitalOcean dashboard, click **Create** > **Droplets**
2. Choose these settings:

| Setting | Value |
|---------|-------|
| **Region** | Choose the closest to Kenya: **London (LON1)** or **Frankfurt (FRA1)** |
| **Image** | Ubuntu 24.04 (LTS) |
| **Plan** | Basic → Regular → **$6/month** (1 GB RAM, 25 GB SSD) |
| **Authentication** | Choose **SSH Key** (recommended) or **Password** |

3. If using **SSH Key**:
   - On your computer, open terminal and run: `ssh-keygen -t ed25519`
   - Press Enter for all prompts
   - Copy your public key: `cat ~/.ssh/id_ed25519.pub`
   - Paste it into the DigitalOcean SSH key field

4. Set hostname to `imani-fellowship`
5. Click **Create Droplet**
6. Note the **IP address** shown (e.g., `164.92.xxx.xxx`)

---

## 3. Connect to Your Server

Open your terminal and connect:

```bash
ssh root@YOUR_DROPLET_IP
```

If using a password, enter it when prompted. If using SSH key, it will connect automatically.

**Create a non-root user** (more secure):

```bash
adduser deploy
usermod -aG sudo deploy
# Copy SSH key to the new user
rsync --archive --chown=deploy:deploy ~/.ssh /home/deploy
```

Switch to the new user:

```bash
su - deploy
```

From now on, always connect as: `ssh deploy@YOUR_DROPLET_IP`

---

## 4. Install System Dependencies

Run these commands one by one:

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python 3.11, pip, and venv
sudo apt install -y python3.11 python3.11-venv python3-pip

# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Install Nginx
sudo apt install -y nginx

# Install Certbot (for free SSL)
sudo apt install -y certbot python3-certbot-nginx

# Install Git
sudo apt install -y git
```

---

## 5. Set Up PostgreSQL Database

```bash
# Switch to the postgres user
sudo -u postgres psql

# Inside the PostgreSQL prompt, run:
CREATE DATABASE imani_fellowship;
CREATE USER imani_user WITH PASSWORD 'choose-a-strong-password-here';
GRANT ALL PRIVILEGES ON DATABASE imani_fellowship TO imani_user;
ALTER USER imani_user CREATEDB;
\q
```

**Remember** the password you chose — you'll need it for the `.env` file.

---

## 6. Deploy the Application

```bash
# Go to the deploy user's home
cd /home/deploy

# Clone the repository
git clone https://github.com/CaptainBett/Imani-Fellowship-AGC-Bomet-Website.git
cd Imani-Fellowship-AGC-Bomet-Website

# Create a Python virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

**Create the `.env` file:**

```bash
nano .env
```

Paste the following (edit the values):

```env
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=generate-a-long-random-string-here

# Database — use the password you set in Step 5
DATABASE_URL=postgresql://imani_user:choose-a-strong-password-here@localhost:5432/imani_fellowship

# TinyMCE
TINYMCE_API_KEY=vdgkimwqqd0orgra0vbzssf3he29kfh22mm4gujnrtfppgfh

# M-Pesa Daraja API
MPESA_CONSUMER_KEY=oB06tjVX2wJ53aw10P1yoIwUmxY6FEClPoQWYAF2QEw3fn1r
MPESA_CONSUMER_SECRET=AOtYzxT8zgKroU6C1VtBNmI6OGwSGjJHZ0dS64RTHCaGpD2ztlcyPEV4IENHr2I1
MPESA_SHORTCODE=4145819
MPESA_PASSKEY=834e541bce9277c813acc08b5d6cf10eb479ebf9382a1cde6c6e10502d1b633d
MPESA_ENV=production
MPESA_CALLBACK_URL=https://yourdomain.co.ke/api/mpesa/callback

# File uploads — will update after setting up Spaces
UPLOAD_STORAGE=local
```

Save: press `Ctrl+X`, then `Y`, then `Enter`.

**To generate a strong SECRET_KEY**, run:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

**Run database migrations:**

```bash
source venv/bin/activate
flask db upgrade
```

---

## 7. Configure Gunicorn (App Server)

Create a systemd service so Gunicorn starts automatically:

```bash
sudo nano /etc/systemd/system/imani.service
```

Paste this:

```ini
[Unit]
Description=Imani Fellowship AGC Website
After=network.target

[Service]
User=deploy
Group=www-data
WorkingDirectory=/home/deploy/Imani-Fellowship-AGC-Bomet-Website
Environment="PATH=/home/deploy/Imani-Fellowship-AGC-Bomet-Website/venv/bin"
ExecStart=/home/deploy/Imani-Fellowship-AGC-Bomet-Website/venv/bin/gunicorn \
    "app:create_app('production')" \
    --bind 127.0.0.1:8000 \
    --workers 2 \
    --access-logfile /var/log/gunicorn/access.log \
    --error-logfile /var/log/gunicorn/error.log
Restart=always

[Install]
WantedBy=multi-user.target
```

Save and close. Then:

```bash
# Create log directory
sudo mkdir -p /var/log/gunicorn
sudo chown deploy:www-data /var/log/gunicorn

# Start and enable the service
sudo systemctl daemon-reload
sudo systemctl start imani
sudo systemctl enable imani

# Check it's running
sudo systemctl status imani
```

You should see "active (running)" in green.

---

## 8. Configure Nginx (Web Server)

```bash
sudo nano /etc/nginx/sites-available/imani
```

Paste this (replace `yourdomain.co.ke` with your actual domain, or use the Droplet IP for now):

```nginx
server {
    listen 80;
    server_name yourdomain.co.ke www.yourdomain.co.ke;

    client_max_body_size 16M;

    # Serve static files directly (faster)
    location /static/ {
        alias /home/deploy/Imani-Fellowship-AGC-Bomet-Website/app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Pass everything else to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:

```bash
# Create a link to enable the site
sudo ln -s /etc/nginx/sites-available/imani /etc/nginx/sites-enabled/

# Remove the default site
sudo rm /etc/nginx/sites-enabled/default

# Test the configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

**Test:** Open your browser and go to `http://YOUR_DROPLET_IP` — you should see the website!

---

## 9. Set Up SSL/HTTPS (Free with Certbot)

**Prerequisites:** Your domain must already be pointing to your Droplet IP (see Step 11).

```bash
sudo certbot --nginx -d yourdomain.co.ke -d www.yourdomain.co.ke
```

Follow the prompts:
1. Enter your email address
2. Agree to terms
3. Choose to redirect HTTP to HTTPS (option 2)

Certbot will:
- Get a free SSL certificate from Let's Encrypt
- Automatically configure Nginx for HTTPS
- Set up auto-renewal (certificates renew every 90 days)

**Test auto-renewal:**

```bash
sudo certbot renew --dry-run
```

---

## 10. Set Up DigitalOcean Spaces (File Uploads)

DigitalOcean Spaces is an S3-compatible storage service for uploaded images.

### Create a Space:

1. In DigitalOcean dashboard, go to **Spaces Object Storage** > **Create a Space**
2. Choose settings:

| Setting | Value |
|---------|-------|
| **Region** | Frankfurt (fra1) or Amsterdam (ams3) |
| **CDN** | Enable (faster image loading) |
| **Name** | `imani-fellowship-uploads` |
| **Permissions** | Private |

3. Click **Create a Space**

### Create API Keys:

1. Go to **API** in the left sidebar
2. Under **Spaces Keys**, click **Generate New Key**
3. Name it `imani-uploads`
4. **Copy both the Key and Secret** — you won't see the secret again!

### Update your `.env` file:

```bash
cd /home/deploy/Imani-Fellowship-AGC-Bomet-Website
nano .env
```

Add/update these lines:

```env
UPLOAD_STORAGE=s3
S3_BUCKET=imani-fellowship-uploads
S3_REGION=fra1
S3_ENDPOINT=https://fra1.digitaloceanspaces.com
S3_ACCESS_KEY=your-spaces-access-key
S3_SECRET_KEY=your-spaces-secret-key
```

Restart the app:

```bash
sudo systemctl restart imani
```

---

## 11. Point Your Domain

### If you bought your domain from a registrar (e.g., KenWebHost, Safaricom, GoDaddy):

1. Log in to your domain registrar's dashboard
2. Go to **DNS Settings** or **Nameservers**
3. Add these DNS records:

| Type | Name | Value |
|------|------|-------|
| **A** | `@` | `YOUR_DROPLET_IP` |
| **A** | `www` | `YOUR_DROPLET_IP` |

4. Wait 15–30 minutes for DNS to propagate

### If you want to use DigitalOcean's DNS:

1. In DigitalOcean dashboard, go to **Networking** > **Domains**
2. Add your domain
3. Add the same A records as above
4. At your domain registrar, change nameservers to:
   - `ns1.digitalocean.com`
   - `ns2.digitalocean.com`
   - `ns3.digitalocean.com`

---

## 12. Update M-Pesa Callback URL

Once your domain is live with HTTPS:

```bash
cd /home/deploy/Imani-Fellowship-AGC-Bomet-Website
nano .env
```

Update this line:

```env
MPESA_CALLBACK_URL=https://yourdomain.co.ke/api/mpesa/callback
```

Replace `yourdomain.co.ke` with your actual domain.

Restart the app:

```bash
sudo systemctl restart imani
```

**Important:** The callback URL **must** use HTTPS. M-Pesa will not send callbacks to HTTP URLs.

---

## 13. Create Admin User

```bash
cd /home/deploy/Imani-Fellowship-AGC-Bomet-Website
source venv/bin/activate
flask shell
```

In the Flask shell:

```python
from app.extensions import db
from app.models.user import User
admin = User(username='admin', email='admin@imanifellowship.co.ke')
admin.set_password('your-secure-password')
db.session.add(admin)
db.session.commit()
exit()
```

Now go to `https://yourdomain.co.ke/auth/login` and log in.

---

## 14. Set Up Automated Backups

### Database Backup (Daily):

```bash
# Create backup directory
sudo mkdir -p /home/deploy/backups
sudo chown deploy:deploy /home/deploy/backups

# Create the backup script
nano /home/deploy/backup_db.sh
```

Paste:

```bash
#!/bin/bash
BACKUP_DIR="/home/deploy/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="imani_fellowship_${TIMESTAMP}.sql.gz"

pg_dump -U imani_user imani_fellowship | gzip > "${BACKUP_DIR}/${FILENAME}"

# Keep only the last 14 backups
ls -t ${BACKUP_DIR}/imani_fellowship_*.sql.gz | tail -n +15 | xargs -r rm
```

Make it executable and set up the daily schedule:

```bash
chmod +x /home/deploy/backup_db.sh

# Add to crontab (runs daily at 2 AM)
crontab -e
```

Add this line:

```
0 2 * * * /home/deploy/backup_db.sh
```

### DigitalOcean Droplet Backups:

1. In the DigitalOcean dashboard, go to your Droplet
2. Click **Backups** tab
3. Enable weekly backups ($1.20/month extra)

---

## 15. Updating the Site

When new code is pushed to GitHub, update the live site:

```bash
# Connect to server
ssh deploy@YOUR_DROPLET_IP

# Go to project directory
cd /home/deploy/Imani-Fellowship-AGC-Bomet-Website

# Pull latest code
git pull origin main

# Activate environment and install any new dependencies
source venv/bin/activate
pip install -r requirements.txt

# Run any new database migrations
flask db upgrade

# Restart the app
sudo systemctl restart imani
```

---

## 16. Troubleshooting

### Site shows "502 Bad Gateway"
Gunicorn is not running:
```bash
sudo systemctl status imani
sudo journalctl -u imani -n 50
```

### Site shows "500 Internal Server Error"
Check the app logs:
```bash
sudo tail -50 /var/log/gunicorn/error.log
```

### M-Pesa payments stay "pending"
1. Check that `MPESA_CALLBACK_URL` in `.env` is correct and uses HTTPS
2. Test the callback URL is reachable: `curl https://yourdomain.co.ke/api/mpesa/callback`
3. Check Gunicorn logs for callback errors

### Database connection errors
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test the connection
psql -U imani_user -d imani_fellowship -h localhost
```

### CSS/images not loading
```bash
# Check Nginx can read static files
ls -la /home/deploy/Imani-Fellowship-AGC-Bomet-Website/app/static/

# Make sure the deploy user is in www-data group
sudo usermod -aG www-data deploy

# Restart Nginx
sudo systemctl restart nginx
```

### Need to check environment variables
```bash
cd /home/deploy/Imani-Fellowship-AGC-Bomet-Website
source venv/bin/activate
flask shell
>>> import os; print(os.environ.get('DATABASE_URL'))
>>> exit()
```

---

## Quick Reference

| What | Command |
|------|---------|
| Start the app | `sudo systemctl start imani` |
| Stop the app | `sudo systemctl stop imani` |
| Restart the app | `sudo systemctl restart imani` |
| Check app status | `sudo systemctl status imani` |
| View app logs | `sudo tail -f /var/log/gunicorn/error.log` |
| Restart Nginx | `sudo systemctl restart nginx` |
| Run migrations | `source venv/bin/activate && flask db upgrade` |
| Open Flask shell | `source venv/bin/activate && flask shell` |
| Manual DB backup | `/home/deploy/backup_db.sh` |
