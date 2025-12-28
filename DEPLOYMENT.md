# Deployment Instructions

This repository is configured for dual deployment:

1. **Render**: Full server-side python environment (Best performance, backend processing).
2. **GitHub Pages**: Client-side WASM environment using `stlite` (Free, static hosting, runs in browser).

---

## 1. Deploy to Render (Recommended for Production)

Render runs the app as a web service. This is ideal if your app uses heavy processing or secrets.

### Option A: One-Click Deploy (Blueprint)

1. Go to your [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** -> **Blueprint**.
3. Connect this repository.
4. Render will auto-detect `render.yaml` and configure Python 3.11, build commands, and start commands.
5. Click **Apply**.
   - Your app will be live at `https://dynamic-probability-calculator.onrender.com` (or similar).

### Option B: Manual Setup

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run main.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
- **Environment Variable**: `PYTHON_VERSION = 3.11.0`

---

## 2. Deploy to GitHub Pages (Static / Serverless)

We use **Stlite** (Streamlit Lite) to run Python directly in the user's browser via WebAssembly.

### Setup (One-time)

1. Go to your GitHub Repository **Settings**.
2. Navigate to **Pages** (on the left sidebar).
3. Under **Build and deployment** > **Source**, select **GitHub Actions** (beta/standard).
   - *Do not* select "Deploy from a branch".
4. The `.github/workflows/stlite_deploy.yml` workflow is already set up to handle the rest.

### Triggering Deployment

- Simply **push to the `main` branch**.
- The Action will build the static site (injecting `main.py` and modules into a web page) and deploy it.
- Your app will be live at `https://<your-username>.github.io/dynamic-probability-calculator/`.

### Note on Stlite

- Since this runs in the browser, some heavy calculations might be slower than Render.
- `stlite` handles `numpy`, `pandas`, `scipy`, and `plotly` well.
- If you add files, ensuring they are listed in `.github/workflows/stlite_deploy.yml` is necessary (specifically the `files` mapping in the HTML generation step).
