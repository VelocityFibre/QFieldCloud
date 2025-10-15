# 🚂 Railway Deployment Guide for QFieldCloud

## 📋 **Prerequisites**
1. **GitHub account** with the QFieldCloud code pushed
2. **Railway account** (sign up at [railway.app](https://railway.app))
3. **Payment method** added to Railway (for $5/month credit)

## 🚀 **Step-by-Step Deployment**

### 1. **Push to GitHub**
```bash
# Make sure you're in the QFieldCloud directory
cd /home/louisdup/VF/Apps/QFieldCloud/QFieldCloud

# Add the new Railway files
git add .
git commit -m "Add Railway configuration for QFieldCloud deployment"

# Push to GitHub (replace with your repo)
git push origin main
```

### 2. **Set up Railway Project**
1. Go to [railway.app](https://railway.app) and login
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Connect your GitHub account
4. Select your QFieldCloud repository
5. Choose the `main` branch
6. Click **"Deploy Now"**

### 3. **Configure Environment Variables**
Railway will automatically build and deploy, but you need to add these variables:

**Go to your project → Settings → Variables** and add:

```bash
# Core Settings (Railway provides PORT automatically)
DJANGO_SETTINGS_MODULE=qfieldcloud.settings
DJANGO_ALLOWED_HOSTS=*
DEBUG=0
ENVIRONMENT=production

# Security (GENERATE NEW ONES!)
SECRET_KEY=your_random_secret_key_here
SALT_KEY=your_random_salt_key_here

# Database
# Railway will automatically provide DATABASE_URL when you add PostgreSQL

# Storage (Optional - if you want S3)
STORAGE_ACCESS_KEY_ID=your_s3_key
STORAGE_SECRET_ACCESS_KEY=your_s3_secret
STORAGE_BUCKET_NAME=your_bucket
STORAGE_REGION_NAME=us-east-1

# Email (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=1
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

### 4. **Add PostgreSQL Database**
1. In your Railway project, click **"New Service"**
2. Select **"PostgreSQL"**
3. Railway will automatically provide `DATABASE_URL`

### 5. **Run Database Migrations**
1. Once deployed, go to your service → **"Logs"**
2. Click **"New Command"** and run:
   ```bash
   python manage.py migrate
   ```

### 6. **Create Superuser**
Run another command in Railway:
```bash
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('admin', 'admin@yourdomain.com', 'your_password')
print('Superuser created!')
"
```

## 🔧 **Troubleshooting**

### **Build Fails?**
- Check the **"Logs"** tab for errors
- Make sure `Dockerfile.web` is in the root directory
- Verify all required files are committed to git

### **Database Connection Issues?**
- Ensure PostgreSQL service is running
- Check that `DATABASE_URL` is available (Railway provides this)
- Run migrations manually if needed

### **Static Files Not Loading?**
- Add this to Railway variables:
  ```bash
  STATIC_URL=/static/
  STATIC_ROOT=/staticfiles/
  ```

## 💰 **Cost Estimate**
- **Free Tier**: $5 credit per month
- **Expected Usage**: $8-15/month depending on traffic
- **Includes**: Web app + PostgreSQL + storage

## 🌐 **Accessing Your App**
Once deployed, Railway will give you a URL like:
- `https://your-app-name.railway.app`
- Admin: `https://your-app-name.railway.app/admin/`

## 🔄 **Automatic Deployments**
- Every push to `main` branch triggers automatic deployment
- Railway handles SSL, scaling, and infrastructure automatically

## 📝 **Notes**
- The QGIS container (spatial processing) is **not** included in this basic setup
- For production use, consider setting up Redis for background jobs
- Monitor your usage in Railway dashboard to avoid unexpected charges

---

**Your QFieldCloud will be live on Railway within minutes! 🎉**