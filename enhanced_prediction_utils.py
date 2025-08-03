import joblib
from preprocessing import preprocess_text
import os
import re

class EnhancedFakeInternshipPredictor:
    def __init__(self, model_dir='model'):
        """
        Initialize the enhanced predictor with trained model and vectorizer
        """
        self.model_path = os.path.join(model_dir, 'fake_job_model.pkl')
        self.vectorizer_path = os.path.join(model_dir, 'tfidf_vectorizer.pkl')
        
        # Load model and vectorizer
        try:
            self.model = joblib.load(self.model_path)
            self.vectorizer = joblib.load(self.vectorizer_path)
            print("Model loaded successfully!")
        except FileNotFoundError:
            print("Model files not found. Please run train_model.py first.")
            self.model = None
            self.vectorizer = None
        
        # Define fake internship patterns (for preprocessed text - no punctuation)
        self.fake_internship_patterns = {
            'certificate_payment': [
                r'pay.*certificate',
                r'certificate.*fee',
                r'certificate.*cost',
                r'certificate.*payment',
                r'pay.*for.*certificate',
                r'certificate.*price',
                r'certificate.*charge',
                r'certificate.*amount',
                r'certificate.*money',
                r'certificate.*dollars',
                r'certificate.*rupees',
                r'certificate.*rs',
                r'certificate.*inr'
            ],
            'virtual_internship_suspicious': [
                r'virtual.*internship.*pay',
                r'online.*internship.*fee',
                r'remote.*internship.*cost',
                r'virtual.*internship.*money',
                r'online.*internship.*payment',
                r'remote.*internship.*charge',
                r'virtual.*internship.*certificate',
                r'online.*internship.*certificate',
                r'remote.*internship.*certificate'
            ],
            'urgent_opportunity': [
                r'urgent.*opportunity',
                r'immediate.*start',
                r'limited.*time',
                r'quick.*money',
                r'fast.*cash',
                r'instant.*payment',
                r'urgent.*hiring',
                r'immediate.*hiring'
            ],
            'no_experience_required': [
                r'no.*experience.*needed',
                r'no.*experience.*required',
                r'no.*skills.*needed',
                r'no.*qualification.*required',
                r'anyone.*can.*apply',
                r'everyone.*welcome',
                r'no.*background.*needed'
            ],
            'suspicious_payment': [
                r'send.*money',
                r'transfer.*funds',
                r'process.*payments',
                r'handle.*money',
                r'bank.*details',
                r'account.*number',
                r'personal.*information',
                r'credit.*card',
                r'debit.*card',
                r'upi.*id',
                r'paytm.*number',
                r'phonepe.*number'
            ],
            'commission_based': [
                r'commission.*based',
                r'commission.*only',
                r'no.*salary',
                r'commission.*payment',
                r'percentage.*commission',
                r'commission.*work'
            ]
        }
    
    def check_fake_patterns(self, text):
        """
        Check for common fake internship patterns
        Returns: (is_fake, pattern_matches, confidence_boost)
        """
        # Text is already preprocessed (lowercase, no punctuation)
        pattern_matches = []
        confidence_boost = 0
        
        for pattern_type, patterns in self.fake_internship_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    pattern_matches.append(f"{pattern_type}: {pattern}")
                    confidence_boost += 15  # Boost confidence for each pattern match
        
        # Special boost for certificate payment patterns
        certificate_matches = [p for p in pattern_matches if 'certificate_payment' in p]
        if certificate_matches:
            confidence_boost += 25  # Extra boost for certificate payment
        
        # Determine if likely fake based on patterns
        is_fake = len(pattern_matches) >= 2 or any('certificate_payment' in p for p in pattern_matches)
        
        return is_fake, pattern_matches, confidence_boost
    
    def predict(self, text, threshold=0.6):
        """
        Enhanced prediction combining ML and rule-based detection
        Returns: (prediction, confidence_score, is_fake, pattern_matches)
        """
        if self.model is None or self.vectorizer is None:
            return None, 0, False, []
        
        try:
            # Preprocess the text
            processed_text = preprocess_text(text)
            
            if not processed_text.strip():
                return "No text to analyze", 0, False, []
            
            # Check for fake patterns first (use processed text for consistency)
            pattern_fake, pattern_matches, confidence_boost = self.check_fake_patterns(processed_text)
            
            # If strong pattern matches, classify as fake
            if pattern_fake and confidence_boost >= 30:
                return 1, 85 + confidence_boost, True, pattern_matches
            
            # Vectorize the text
            text_vector = self.vectorizer.transform([processed_text])
            
            # Get prediction probability
            proba = self.model.predict_proba(text_vector)[0]
            
            # Get prediction (0 = real, 1 = fake)
            prediction = self.model.predict(text_vector)[0]
            
            # Calculate confidence score
            if prediction == 0:  # Real
                confidence_score = proba[0] * 100
                is_fake = False
            else:  # Fake
                confidence_score = proba[1] * 100
                is_fake = True
            
            # Apply pattern-based confidence boost
            if pattern_matches:
                if is_fake:
                    confidence_score = min(100, confidence_score + confidence_boost)
                else:
                    # If ML says real but patterns suggest fake, reduce confidence
                    confidence_score = max(0, confidence_score - confidence_boost)
                    if confidence_boost >= 20:
                        is_fake = True
                        prediction = 1
            
            return prediction, confidence_score, is_fake, pattern_matches
            
        except Exception as e:
            print(f"Error making prediction: {str(e)}")
            return None, 0, False, []
    
    def get_prediction_result(self, text, threshold=0.4):
        """
        Get formatted prediction result with pattern analysis
        """
        prediction, confidence_score, is_fake, pattern_matches = self.predict(text, threshold)
        
        if prediction is None:
            return "Error", 0, "❌", []
        
        # Determine if it's likely fake based on threshold
        if is_fake and confidence_score > (threshold * 100):
            result = "Likely FAKE ❌"
        else:
            result = "Likely REAL ✅"
        
        return result, confidence_score, "❌" if is_fake else "✅", pattern_matches

    def analyze_salary_range(self, text):
        """Analyze salary ranges for unrealistic promises"""
        text_lower = text.lower()
        
        # Look for salary patterns
        salary_patterns = [
            r'\$\d{1,3}(?:,\d{3})*(?:-\d{1,3}(?:,\d{3})*)?\s*(?:per\s+)?(?:hour|day|week|month|year)',
            r'\d{1,3}(?:,\d{3})*(?:-\d{1,3}(?:,\d{3})*)?\s*(?:dollars?|usd|inr|rupees?)\s*(?:per\s+)?(?:hour|day|week|month|year)',
            r'(?:salary|pay|compensation|earnings?)\s*(?:of\s+)?\$\d{1,3}(?:,\d{3})*(?:-\d{1,3}(?:,\d{3})*)?'
        ]
        
        suspicious_indicators = [
            'no experience required',
            'work from home',
            'immediate start',
            'quick money',
            'fast cash',
            'easy money',
            'high salary',
            'excellent pay',
            'great compensation'
        ]
        
        salary_found = any(re.search(pattern, text_lower) for pattern in salary_patterns)
        suspicious_terms = sum(1 for term in suspicious_indicators if term in text_lower)
        
        if salary_found and suspicious_terms >= 3:
            return "⚠️ HIGH RISK: Unrealistic salary promises detected"
        elif salary_found and suspicious_terms >= 1:
            return "⚠️ MEDIUM RISK: Potentially unrealistic salary"
        elif salary_found:
            return "✅ NORMAL: Standard salary range"
        else:
            return "ℹ️ INFO: No specific salary mentioned"

    def analyze_internship_description_quality(self, text):
        """Rate the professionalism of internship descriptions"""
        text_lower = text.lower()
        
        # Professional indicators
        professional_indicators = [
            'requirements', 'qualifications', 'responsibilities', 'duties',
            'experience', 'skills', 'education', 'degree', 'certification',
            'team', 'collaboration', 'leadership', 'management',
            'project', 'development', 'analysis', 'strategy'
        ]
        
        # Unprofessional indicators
        unprofessional_indicators = [
            'urgent', 'immediate', 'quick', 'fast', 'easy',
            'no experience needed', 'anyone can apply', 'everyone welcome',
            'work from anywhere', 'flexible hours', 'no pressure',
            'commission only', 'no salary', 'payment required'
        ]
        
        professional_count = sum(1 for term in professional_indicators if term in text_lower)
        unprofessional_count = sum(1 for term in unprofessional_indicators if term in text_lower)
        
        total_words = len(text.split())
        professional_ratio = professional_count / max(total_words, 1) * 100
        unprofessional_ratio = unprofessional_count / max(total_words, 1) * 100
        
        if professional_ratio > 2 and unprofessional_ratio < 1:
            return "✅ EXCELLENT: Professional internship description"
        elif professional_ratio > 1 and unprofessional_ratio < 2:
            return "✅ GOOD: Well-structured internship description"
        elif unprofessional_ratio > 2:
            return "⚠️ POOR: Unprofessional internship description"
        else:
            return "ℹ️ AVERAGE: Standard internship description"

    def analyze_interview_process(self, text):
        """Identify suspicious interview procedures"""
        text_lower = text.lower()
        
        # Suspicious interview patterns
        suspicious_patterns = [
            'no interview required',
            'immediate hiring',
            'quick hiring process',
            'no background check',
            'no verification needed',
            'start immediately',
            'no questions asked',
            'automatic approval',
            'instant approval',
            'no formal interview',
            'chat interview only',
            'text interview',
            'whatsapp interview'
        ]
        
        # Legitimate interview patterns
        legitimate_patterns = [
            'interview process',
            'multiple rounds',
            'technical interview',
            'behavioral interview',
            'background check',
            'reference check',
            'skill assessment',
            'coding test',
            'presentation',
            'case study'
        ]
        
        suspicious_count = sum(1 for pattern in suspicious_patterns if pattern in text_lower)
        legitimate_count = sum(1 for pattern in legitimate_patterns if pattern in text_lower)
        
        if suspicious_count >= 2:
            return "🚨 HIGH RISK: Suspicious interview process detected"
        elif suspicious_count >= 1:
            return "⚠️ MEDIUM RISK: Potentially suspicious interview process"
        elif legitimate_count >= 2:
            return "✅ GOOD: Standard interview process"
        else:
            return "ℹ️ INFO: No specific interview details mentioned" 