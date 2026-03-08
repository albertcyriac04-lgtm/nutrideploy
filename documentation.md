# NutriDiet: AI-Powered Personalized Diet & Health Tracker
## Project Documentation (MCA Mini-Project)

**NutriDiet** is a sophisticated, data-driven web application designed to help users manage their health through personalized nutrition tracking, AI-driven meal planning, and Machine Learning weight forecasting.

---

## 1. Executive Summary
NutriDiet goes beyond traditional calorie counting by integrating **Google Gemini AI** for culturalized (Indian) meal planning and **Scikit-Learn (ML)** for predictive health analytics. It provides a premium user experience with real-time hydration tracking, professional PDF/Excel reporting, and secure Multi-Factor Authentication (MFA).

## 2. Key Features

### 🤖 AI Nutrition Coach (Gemini 2.0 Flash)
- **Natural Language Chat**: A conversational interface for health advice, recipe ideas, and grocery tips.
- **Context Awareness**: The AI understands the user's specific health profile (BMR, TDEE, weight goals) during the conversation.

### 🍱 AI-Powered Indian Diet Planner
- **Cultural Personalization**: Generates 1-day Indian meal plans (Breakfast, Lunch, Dinner, Snacks).
- **Dietary Preferences**: Supports Vegetarian, Non-Vegetarian, and Vegan options.
- **Daily Persistence**: Plans are saved in the database to track dietary habits over time.

### 📈 Machine Learning Weight Analytics
- **Linear Regression Forecasting**: Analyzes weight history to predict weight 7 days into the future.
- **Goal Attainment Prediction**: Uses the trend slope to estimate the exact date the user will reach their target weight.
- **Statistical Metrics**: Displays R-Squared (Confidence) and Slope Coefficient for academic/technical evaluation.

### 💧 Smart Hydration Tracking
- **Individualized Targets**: Automatically calculates water needs (~35ml/kg + activity adjustment).
- **Interactive Logging**: Real-time glass-by-glass tracking with progress visualization.
- **Target Completion**: Monitors daily goal attainment for reporting.

### 📄 Professional Data Reporting
- **Multi-Format Export**: Generates reports in **PDF** and **Excel**.
- **Periodic Filtering**: Options for Weekly, Monthly, and Yearly reports.
- **AI Executive Summary**: Gemini analyzes the user's performance and writes a professional health summary at the end of every report.

### 🔐 Security & User Management
- **Multi-Factor Authentication (MFA)**: Enhanced security using the `django-two-factor-auth` library.
- **Profile Management**: Customizable health metrics (Age, Gender, Activity Level, Target Weight).

---

## 3. Technology Stack

- **Backend**: Python 3.13, Django 5.1.4
- **Database**: SQLite (Development) / PostgreSQL (Production ready)
- **Artificial Intelligence**: Google Gemini API (`google-generativeai`)
- **Machine Learning**: Scikit-Learn (Linear Regression), NumPy, Pandas
- **Reports**: ReportLab (PDF), OpenPyXL (Excel)
- **Frontend**: Vanilla HTML5, CSS3 (Custom Design System), JavaScript (AJAX/Fetch)
- **Styling**: Tailwind CSS (via CDN) & Custom CSS Transitions

---

## 4. System Architecture (MVC)

### Models (`api/models.py`)
- `UserProfile`: Core health metrics and dietary preferences.
- `ConsumptionLog`: Daily food intake and calorie data.
- `WeightRecord`: Historical weight entries.
- `WaterLog`: Daily hydration tracking.
- `DailyDietPlan`: Persistent AI-generated meals.

### Intelligence Layer
- `api/ml_utils.py`: Contains the `predict_weight_trend` function using Scikit-Learn.
- `api/ai_utils.py`: Manages Gemini API interactions for diets and report summaries.

### Reporting Layer (`api/report_utils.py`)
- Handles the construction of PDF tables and Excel workbooks for exports.

---

## 5. Setup & Installation

1. **Clone the project & install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure Environment**:
   Create a `.env` file with:
   ```env
   SECRET_KEY=your_django_key
   GEMINI_API_KEY=your_google_gemini_key
   DB_NAME=nutridiet_db
   ```
3. **Initialize Database**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. **Run Server**:
   ```bash
   python manage.py runserver
   ```

---

## 6. Future Enhancements
- **Wearable Integration**: Sync data from Apple Health or Google Fit.
- **Computer Vision**: Food recognition via uploaded meal photos.
- **Social Features**: Community challenges and leaderboard systems.

---
**Developed for NutriDiet MCA Project © 2025**
