from flask import Flask, render_template, request, jsonify, send_file
import os
from enhanced_prediction_utils import EnhancedFakeJobPredictor
from ocr_utils import extract_text_from_image, is_valid_image, get_ocr_status
from scraping_utils import extract_text_from_url, is_valid_url
import json
from datetime import datetime
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Initialize enhanced predictor
predictor = EnhancedFakeJobPredictor()

# Enhanced company database with more comprehensive information
ENHANCED_COMPANY_DATABASE = {
    # Fraudulent Companies
    "fakecorp": {
        "name": "FakeCorp Inc", 
        "fraud_score": 95, 
        "reports": 150, 
        "last_updated": "2024-01-15",
        "domain_age": "2 months",
        "social_media": "Limited/None",
        "contact_verification": "Failed",
        "industry": "Technology",
        "location": "Unknown",
        "website": "fakecorp-scam.com",
        "red_flags": ["No physical address", "Fake testimonials", "Payment required upfront"]
    },
    "scamtech": {
        "name": "ScamTech Solutions", 
        "fraud_score": 88, 
        "reports": 89, 
        "last_updated": "2024-01-10",
        "domain_age": "3 months",
        "social_media": "None",
        "contact_verification": "Failed",
        "industry": "IT Services",
        "location": "Virtual",
        "website": "scamtech-fake.net",
        "red_flags": ["Virtual office only", "No employee reviews", "Suspicious payment methods"]
    },
    "phishco": {
        "name": "PhishCo Ltd", 
        "fraud_score": 92, 
        "reports": 234, 
        "last_updated": "2024-01-12",
        "domain_age": "1 month",
        "social_media": "Fake profiles",
        "contact_verification": "Failed",
        "industry": "Consulting",
        "location": "International",
        "website": "phishco-scam.org",
        "red_flags": ["International scam", "Fake social media", "Data harvesting"]
    },
    
    # Legitimate Companies
    "google": {
        "name": "Google", 
        "fraud_score": 5, 
        "reports": 2, 
        "last_updated": "2024-01-15",
        "domain_age": "25+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Technology",
        "location": "Mountain View, CA",
        "website": "google.com",
        "green_flags": ["Established company", "Verified contact info", "Positive reviews"]
    },
    "microsoft": {
        "name": "Microsoft", 
        "fraud_score": 3, 
        "reports": 1, 
        "last_updated": "2024-01-15",
        "domain_age": "30+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Technology",
        "location": "Redmond, WA",
        "website": "microsoft.com",
        "green_flags": ["Fortune 500 company", "Verified contact info", "Excellent reputation"]
    },
    "amazon": {
        "name": "Amazon", 
        "fraud_score": 6, 
        "reports": 5, 
        "last_updated": "2024-01-15",
        "domain_age": "25+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "E-commerce",
        "location": "Seattle, WA",
        "website": "amazon.com",
        "green_flags": ["Global company", "Verified contact info", "Established reputation"]
    }
}

# Multi-language support
LANGUAGES = {
    'en': {
        'title': 'JobGuardian Pro - Advanced Job Fraud Detection',
        'tagline': 'Advanced AI-Powered Job Fraud Detection & Company Verification',
        'job_detection': 'Job Detection',
        'company_search': 'Company Search',
        'job_analysis': 'Job Posting Analysis',
        'analysis_desc': 'Analyze job postings for potential fraud using advanced AI and pattern recognition.',
        'direct_text': 'Direct Text',
        'url_extraction': 'URL Extraction',
        'paste_placeholder': 'Paste the job posting text here...',
        'analyze_btn': 'Analyze Job Posting',
        'url_placeholder': 'Enter job posting URL...',
        'extract_btn': 'Extract & Analyze',
        'company_database': 'Company Fraud Database',
        'company_desc': 'Search our comprehensive database to check if a company has been reported for fraud.',
        'company_placeholder': 'Enter company name...',
        'search_btn': 'Search',
        'results': 'Analysis Results',
        'company_info': 'Company Information',
        'footer_copyright': '© 2024 JobGuardian Pro. Built with advanced AI and machine learning.',
        'disclaimer': '⚠️ This tool is for educational purposes. Always verify job postings through official channels.',
        'analyzing': 'Analyzing...',
        'likely_fake': 'Likely FAKE ❌',
        'likely_real': 'Likely REAL ✅',
        'confidence': 'Confidence',
        'words_analyzed': 'Words Analyzed',
        'suspicious_patterns': 'Suspicious Patterns Detected',
        'fraud_detected': 'FRAUD DETECTED',
        'legitimate_company': 'LEGITIMATE COMPANY',
        'fraud_score': 'Fraud Score',
        'reports': 'Reports',
        'last_updated': 'Last Updated',
        'domain_age': 'Domain Age',
        'social_media': 'Social Media',
        'contact_verification': 'Contact Verification',
        'industry': 'Industry',
        'location': 'Location',
        'website': 'Website',
        'red_flags': 'Red Flags',
        'green_flags': 'Green Flags',
        'export_pdf': 'Export PDF Report',
        'salary_analysis': 'Salary Analysis',
        'job_quality': 'Job Description Quality',
        'interview_analysis': 'Interview Process Analysis',
        'document_analysis': 'Document Analysis',
        'linkedin_integration': 'LinkedIn Integration',
        'indeed_integration': 'Indeed Integration',
        'glassdoor_integration': 'Glassdoor Integration'
    },
    'hi': {
        'title': 'जॉबगार्डियन प्रो - उन्नत नौकरी धोखाधड़ी पहचान',
        'tagline': 'उन्नत AI-संचालित नौकरी धोखाधड़ी पहचान और कंपनी सत्यापन',
        'job_detection': 'नौकरी पहचान',
        'company_search': 'कंपनी खोज',
        'job_analysis': 'नौकरी पोस्टिंग विश्लेषण',
        'analysis_desc': 'उन्नत AI और पैटर्न पहचान का उपयोग करके नौकरी पोस्टिंग का विश्लेषण करें।',
        'direct_text': 'सीधा टेक्स्ट',
        'url_extraction': 'URL निष्कर्षण',
        'paste_placeholder': 'नौकरी पोस्टिंग टेक्स्ट यहाँ पेस्ट करें...',
        'analyze_btn': 'नौकरी पोस्टिंग विश्लेषण करें',
        'url_placeholder': 'नौकरी पोस्टिंग URL दर्ज करें...',
        'extract_btn': 'निष्कर्षण और विश्लेषण',
        'company_database': 'कंपनी धोखाधड़ी डेटाबेस',
        'company_desc': 'जांचें कि क्या कंपनी को धोखाधड़ी के लिए रिपोर्ट किया गया है।',
        'company_placeholder': 'कंपनी का नाम दर्ज करें...',
        'search_btn': 'खोजें',
        'results': 'विश्लेषण परिणाम',
        'company_info': 'कंपनी की जानकारी',
        'footer_copyright': '© 2024 जॉबगार्डियन प्रो। उन्नत AI और मशीन लर्निंग के साथ बनाया गया।',
        'disclaimer': '⚠️ यह उपकरण शैक्षिक उद्देश्यों के लिए है। हमेशा आधिकारिक चैनलों के माध्यम से नौकरी पोस्टिंग की जांच करें।',
        'analyzing': 'विश्लेषण कर रहा है...',
        'likely_fake': 'संभवतः नकली ❌',
        'likely_real': 'संभवतः वास्तविक ✅',
        'confidence': 'विश्वास',
        'words_analyzed': 'विश्लेषित शब्द',
        'suspicious_patterns': 'संदिग्ध पैटर्न पाए गए',
        'fraud_detected': 'धोखाधड़ी पाई गई',
        'legitimate_company': 'वैध कंपनी',
        'fraud_score': 'धोखाधड़ी स्कोर',
        'reports': 'रिपोर्ट',
        'last_updated': 'अंतिम अपडेट',
        'domain_age': 'डोमेन आयु',
        'social_media': 'सोशल मीडिया',
        'contact_verification': 'संपर्क सत्यापन',
        'industry': 'उद्योग',
        'location': 'स्थान',
        'website': 'वेबसाइट',
        'red_flags': 'लाल झंडे',
        'green_flags': 'हरे झंडे',
        'export_pdf': 'PDF रिपोर्ट निर्यात करें',
        'salary_analysis': 'वेतन विश्लेषण',
        'job_quality': 'नौकरी विवरण गुणवत्ता',
        'interview_analysis': 'साक्षात्कार प्रक्रिया विश्लेषण',
        'document_analysis': 'दस्तावेज़ विश्लेषण',
        'linkedin_integration': 'LinkedIn एकीकरण',
        'indeed_integration': 'Indeed एकीकरण',
        'glassdoor_integration': 'Glassdoor एकीकरण'
    },
    'bn': {
        'title': 'জবগার্ডিয়ান প্রো - উন্নত চাকরি প্রতারণা সনাক্তকরণ',
        'tagline': 'উন্নত AI-চালিত চাকরি প্রতারণা সনাক্তকরণ এবং কোম্পানি যাচাইকরণ',
        'job_detection': 'চাকরি সনাক্তকরণ',
        'company_search': 'কোম্পানি অনুসন্ধান',
        'job_analysis': 'চাকরি পোস্টিং বিশ্লেষণ',
        'analysis_desc': 'উন্নত AI এবং প্যাটার্ন সনাক্তকরণ ব্যবহার করে চাকরি পোস্টিং বিশ্লেষণ করুন।',
        'direct_text': 'সরাসরি টেক্সট',
        'url_extraction': 'URL নিষ্কর্ষণ',
        'paste_placeholder': 'চাকরি পোস্টিং টেক্সট এখানে পেস্ট করুন...',
        'analyze_btn': 'চাকরি পোস্টিং বিশ্লেষণ করুন',
        'url_placeholder': 'চাকরি পোস্টিং URL লিখুন...',
        'extract_btn': 'নিষ্কর্ষণ এবং বিশ্লেষণ',
        'company_database': 'কোম্পানি প্রতারণা ডেটাবেস',
        'company_desc': 'কোম্পানিকে প্রতারণার জন্য রিপোর্ট করা হয়েছে কিনা তা যাচাই করুন।',
        'company_placeholder': 'কোম্পানির নাম লিখুন...',
        'search_btn': 'অনুসন্ধান করুন',
        'results': 'বিশ্লেষণ ফলাফল',
        'company_info': 'কোম্পানির তথ্য',
        'footer_copyright': '© 2024 জবগার্ডিয়ান প্রো। উন্নত AI এবং মেশিন লার্নিং দিয়ে তৈরি।',
        'disclaimer': '⚠️ এই টুলটি শিক্ষামূলক উদ্দেশ্যে। সর্বদা সরকারি চ্যানেলের মাধ্যমে চাকরি পোস্টিং যাচাই করুন।',
        'analyzing': 'বিশ্লেষণ করছে...',
        'likely_fake': 'সম্ভবত জাল ❌',
        'likely_real': 'সম্ভবত আসল ✅',
        'confidence': 'আত্মবিশ্বাস',
        'words_analyzed': 'বিশ্লেষিত শব্দ',
        'suspicious_patterns': 'সন্দেহজনক প্যাটার্ন পাওয়া গেছে',
        'fraud_detected': 'প্রতারণা সনাক্ত হয়েছে',
        'legitimate_company': 'বৈধ কোম্পানি',
        'fraud_score': 'প্রতারণা স্কোর',
        'reports': 'রিপোর্ট',
        'last_updated': 'সর্বশেষ আপডেট',
        'domain_age': 'ডোমেন বয়স',
        'social_media': 'সামাজিক মাধ্যম',
        'contact_verification': 'যোগাযোগ যাচাইকরণ',
        'industry': 'শিল্প',
        'location': 'অবস্থান',
        'website': 'ওয়েবসাইট',
        'red_flags': 'লাল পতাকা',
        'green_flags': 'সবুজ পতাকা',
        'export_pdf': 'PDF রিপোর্ট রপ্তানি করুন',
        'salary_analysis': 'বেতন বিশ্লেষণ',
        'job_quality': 'চাকরির বিবরণ গুণমান',
        'interview_analysis': 'সাক্ষাত্কার প্রক্রিয়া বিশ্লেষণ',
        'document_analysis': 'নথি বিশ্লেষণ',
        'linkedin_integration': 'LinkedIn ইন্টিগ্রেশন',
        'indeed_integration': 'Indeed ইন্টিগ্রেশন',
        'glassdoor_integration': 'Glassdoor ইন্টিগ্রেশন'
    }
}

@app.route('/')
def index():
    lang = request.args.get('lang', 'en')
    return render_template('index.html', lang=lang, translations=LANGUAGES.get(lang, LANGUAGES['en']))

@app.route('/detect', methods=['POST'])
def detect_job():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text.strip():
            return jsonify({'error': 'No text provided'}), 400
        
        # Get prediction with pattern analysis
        result, confidence_score, icon, pattern_matches = predictor.get_prediction_result(text)
        
        # AI-Powered Features
        salary_analysis = predictor.analyze_salary_range(text)
        job_quality_score = predictor.analyze_job_description_quality(text)
        interview_analysis = predictor.analyze_interview_process(text)
        
        return jsonify({
            'result': result,
            'confidence_score': round(confidence_score, 1),
            'icon': icon,
            'pattern_matches': pattern_matches,
            'word_count': len(text.split()),
            'salary_analysis': salary_analysis,
            'job_quality_score': job_quality_score,
            'interview_analysis': interview_analysis
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search_company', methods=['POST'])
def search_company():
    try:
        data = request.get_json()
        company_name = data.get('company_name', '').lower().strip()
        
        if not company_name:
            return jsonify({'error': 'No company name provided'}), 400
        
        # Search in enhanced company database
        if company_name in ENHANCED_COMPANY_DATABASE:
            company_data = ENHANCED_COMPANY_DATABASE[company_name]
            return jsonify({
                'found': True,
                'is_fraud': company_data['fraud_score'] > 50,
                'company_data': company_data
            })
        
        # Search for partial matches
        matches = {k: v for k, v in ENHANCED_COMPANY_DATABASE.items() 
                  if company_name in k or company_name in v['name'].lower()}
        
        if matches:
            first_match = list(matches.items())[0]
            return jsonify({
                'found': True,
                'is_fraud': first_match[1]['fraud_score'] > 50,
                'company_data': first_match[1],
                'partial_match': True
            })
        
        # Company not found
        return jsonify({
            'found': False,
            'message': 'Company not found in our database. This could be a new company or the name might be misspelled.'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/extract_url', methods=['POST'])
def extract_url():
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        
        if not is_valid_url(url):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        extracted_text = extract_text_from_url(url)
        
        if extracted_text:
            return jsonify({
                'success': True,
                'text': extracted_text,
                'word_count': len(extracted_text.split())
            })
        else:
            return jsonify({'error': 'Could not extract text from URL'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze_linkedin', methods=['POST'])
def analyze_linkedin():
    try:
        data = request.get_json()
        linkedin_url = data.get('linkedin_url', '')
        
        if not linkedin_url:
            return jsonify({'error': 'No LinkedIn URL provided'}), 400
        
        # Extract text from LinkedIn job posting
        extracted_text = extract_text_from_url(linkedin_url)
        
        if extracted_text:
            # Get prediction with pattern analysis
            result, confidence_score, icon, pattern_matches = predictor.get_prediction_result(extracted_text)
            
            # AI-Powered Features
            salary_analysis = predictor.analyze_salary_range(extracted_text)
            job_quality_score = predictor.analyze_job_description_quality(extracted_text)
            interview_analysis = predictor.analyze_interview_process(extracted_text)
            
            return jsonify({
                'success': True,
                'result': result,
                'confidence_score': round(confidence_score, 1),
                'icon': icon,
                'pattern_matches': pattern_matches,
                'word_count': len(extracted_text.split()),
                'salary_analysis': salary_analysis,
                'job_quality_score': job_quality_score,
                'interview_analysis': interview_analysis,
                'source': 'LinkedIn'
            })
        else:
            return jsonify({'error': 'Could not extract text from LinkedIn URL'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export_pdf', methods=['POST'])
def export_pdf():
    try:
        data = request.get_json()
        analysis_data = data.get('analysis_data', {})
        
        # Create PDF report
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1
        )
        story.append(Paragraph("JobGuardian Pro - Analysis Report", title_style))
        story.append(Spacer(1, 20))
        
        # Analysis Results
        story.append(Paragraph("Analysis Results", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        result_data = [
            ['Metric', 'Value'],
            ['Result', analysis_data.get('result', 'N/A')],
            ['Confidence Score', f"{analysis_data.get('confidence_score', 0)}%"],
            ['Words Analyzed', analysis_data.get('word_count', 0)],
            ['Patterns Detected', len(analysis_data.get('pattern_matches', []))]
        ]
        
        result_table = Table(result_data)
        result_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(result_table)
        story.append(Spacer(1, 20))
        
        # AI Analysis
        if 'salary_analysis' in analysis_data:
            story.append(Paragraph("AI-Powered Analysis", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            ai_data = [
                ['Analysis Type', 'Result'],
                ['Salary Analysis', analysis_data.get('salary_analysis', 'N/A')],
                ['Job Quality Score', analysis_data.get('job_quality_score', 'N/A')],
                ['Interview Analysis', analysis_data.get('interview_analysis', 'N/A')]
            ]
            
            ai_table = Table(ai_data)
            ai_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(ai_table)
            story.append(Spacer(1, 20))
        
        # Patterns Detected
        if analysis_data.get('pattern_matches'):
            story.append(Paragraph("Suspicious Patterns Detected", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            for pattern in analysis_data['pattern_matches']:
                story.append(Paragraph(f"• {pattern}", styles['Normal']))
            
            story.append(Spacer(1, 20))
        
        # Footer
        story.append(Paragraph("Generated by JobGuardian Pro", styles['Normal']))
        story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Paragraph("⚠️ This report is for educational purposes only.", styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"jobguardian_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mimetype='application/pdf'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 