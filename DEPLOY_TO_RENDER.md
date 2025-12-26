# Deploy to Render - One-Click Setup

## Option 1: Deploy from Dashboard with Blueprint (Recommended)

1. **Go to Render Dashboard**: <https://dashboard.render.com/>
2. **Click "New +" → "Blueprint"**
3. **Connect Repository**: Select `dynamic-probability-calculator`
4. **Auto-Configuration**: Render will detect `render.yaml` and configure everything automatically
5. **Click "Apply"** - Done! ✅

The Blueprint (`render.yaml`) already contains all settings:

- Python 3.11
- Auto-installs dependencies from `requirements.txt`
- Starts Streamlit on the correct port
- Configured for web deployment

**Deployment URL will be**: `https://dynamic-probability-calculator.onrender.com`

---

## Option 2: Manual Web Service Creation

If you prefer manual setup:

1. Go to <https://dashboard.render.com/>
2. Click **"New +"** → **"Web Service"**
3. Select repository: `dynamic-probability-calculator`
4. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run main.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
   - **Environment**: Python 3

---

## Auto-Deploy

With the Blueprint, any push to `main` will automatically redeploy! 🚀
