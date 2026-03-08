from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io
import os

def generate_pdf():
    doc = SimpleDocTemplate("nutridiet_technical_guide.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leftIndent=20,
        spaceBefore=5,
        spaceAfter=5
    )
    
    elements = []
    
    # --- TITLE PAGE ---
    elements.append(Spacer(1, 100))
    title_style = ParagraphStyle('MainTitle', parent=styles['Title'], fontSize=28, spaceAfter=20)
    elements.append(Paragraph("NutriDiet Technical Reference", title_style))
    elements.append(Paragraph("Comprehensive Module & File Breakdown", styles['Heading2']))
    elements.append(Paragraph("MCA Mini-Project Documentation", styles['Normal']))
    elements.append(Spacer(1, 50))
    elements.append(Paragraph("This document provides a line-level explanation of the project structure, logic, and implementation details.", styles['Italic']))
    elements.append(PageBreak())
    
    # --- PROJECT STRUCTURE ---
    elements.append(Paragraph("1. Project Architecture", styles['Heading1']))
    elements.append(Paragraph("The project follows the Django MVT (Model-View-Template) pattern, enhanced with an Intelligence Layer (AI/ML) and a Reporting Module.", styles['Normal']))
    
    structure_data = [
        ['Folder/File', 'Purpose'],
        ['nutrigem_backend/', 'Project configuration (settings, secret keys, URL routing).'],
        ['api/', 'Core application logic, models, AI, ML, and business rules.'],
        ['templates/', 'UI Layer (HTML5/Jinja2 templates).'],
        ['static/', 'Frontend assets (CSS, Vanilla JavaScript).'],
        ['api/ml_utils.py', 'Machine Learning engine using Scikit-Learn.'],
        ['api/ai_utils.py', 'Generative AI integration (Google Gemini).'],
        ['api/report_utils.py', 'Export system for PDF and Excel reports.'],
    ]
    
    t = Table(structure_data, colWidths=[150, 350])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 20))
    
    # --- MODULE BREAKDOWN ---
    elements.append(Paragraph("2. Detailed Module Breakdown", styles['Heading1']))
    
    # Models
    elements.append(Paragraph("2.1 Data Models (api/models.py)", styles['Heading2']))
    elements.append(Paragraph("Defines how health data is stored in the database.", styles['Normal']))
    elements.append(Paragraph("Key Classes:", styles['Heading3']))
    elements.append(Paragraph("<b>- UserProfile:</b> Stores age, height, weight, activity levels, and dietary preferences (Veg/Non-Veg). Tracks calculated BMR and TDEE.", styles['Normal']))
    elements.append(Paragraph("<b>- WaterLog:</b> Tracks daily water glass counts and completion status.", styles['Normal']))
    elements.append(Paragraph("<b>- DailyDietPlan:</b> Caches AI-generated Indian meal plans to prevent duplicate API calls.", styles['Normal']))
    
    # Logic: views_frontend.py
    elements.append(Paragraph("2.2 Application Logic (api/views_frontend.py)", styles['Heading2']))
    elements.append(Paragraph("This is the 'Brain' of the application. It handles routing and backend requests.", styles['Normal']))
    elements.append(Paragraph("Key Logic Blocks:", styles['Heading3']))
    elements.append(Paragraph("<b>- index():</b> Gathers all dashboard data, calculates stats, and triggers ML predictions.", styles['Normal']))
    elements.append(Paragraph("<b>- ai_coach_api():</b> Manages the chat interface with Gemini. It includes session management to keep the assistant context-aware.", styles['Normal']))
    elements.append(Paragraph("<b>- export_report_api():</b> Filters data by date (weekly/monthly) and generates requested report formats.", styles['Normal']))
    
    # Intelligence: ML
    elements.append(Paragraph("2.3 Machine Learning (api/ml_utils.py)", styles['Heading2']))
    elements.append(Paragraph("<b>Logic Explanation:</b>", styles['Normal']))
    elements.append(Paragraph("The system uses <i>Linear Regression</i> to map time (x) vs weight (y).", styles['Italic']))
    elements.append(Paragraph("Line 25: <i>model.fit(X, y)</i> - Trains the model on historical records.", code_style))
    elements.append(Paragraph("Line 32: <i>attainment_date = (target - intercept) / slope</i> - Predictive math to find the goal date.", code_style))
    
    # AI: Gemini
    elements.append(Paragraph("2.4 Generative AI (api/ai_utils.py)", styles['Heading2']))
    elements.append(Paragraph("This module uses Gemini 2.0 Flash to generate high-quality text responses.", styles['Normal']))
    elements.append(Paragraph("Line 15: <i>model.generate_content(prompt)</i> - Sends user profile + cultural context to AI.", code_style))
    elements.append(Paragraph("Line 50: <i>json.loads(resp_text)</i> - Parses AI response into structured meal data.", code_style))
    
    elements.append(PageBreak())
    
    # --- HOW TO CHANGE ---
    elements.append(Paragraph("3. How to Modify the Project", styles['Heading1']))
    elements.append(Paragraph("<b>- To change calorie logic:</b> Update <i>api/models.py -> calculate_dashboard_stats()</i>.", styles['Normal']))
    elements.append(Paragraph("<b>- To add a new UI section:</b> Modify <i>templates/index.html</i> using Tailwind CSS classes.", styles['Normal']))
    elements.append(Paragraph("<b>- To tweak AI behavior:</b> Edit the system prompts in <i>api/views_frontend.py -> ai_coach_api()</i>.", styles['Normal']))
    
    elements.append(Spacer(1, 50))
    elements.append(Paragraph("End of Technical Guide", styles['Italic']))
    
    doc.build(elements)
    print("PDF Generated: nutridiet_technical_guide.pdf")

if __name__ == "__main__":
    generate_pdf()
