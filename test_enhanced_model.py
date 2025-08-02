from enhanced_prediction_utils import EnhancedFakeJobPredictor

def test_enhanced_model():
    """Test the enhanced model with fake internship patterns"""
    print("Testing Enhanced Fake Job Posting Detector")
    print("=" * 60)
    
    # Initialize enhanced predictor
    predictor = EnhancedFakeJobPredictor()
    
    # Test cases specifically for fake internships
    test_cases = [
        {
            "name": "Fake Virtual Internship with Certificate Payment",
            "text": "Virtual Internship Opportunity! Join our online internship program. You need to pay $50 for the certificate upon completion. No experience required. Work from home and get certified. Limited time offer!"
        },
        {
            "name": "Fake Internship Asking for Money",
            "text": "Remote Data Science Internship. Pay Rs. 2000 for certificate fee. Virtual internship with flexible hours. Certificate will be provided after payment. No background check needed."
        },
        {
            "name": "Suspicious Online Internship",
            "text": "Online Marketing Internship - Immediate Start! Pay certificate fee of 1500 rupees. Virtual internship opportunity. Send your bank details for payment processing. Commission based work."
        },
        {
            "name": "Real Internship (for comparison)",
            "text": "Software Engineering Internship at Microsoft. We are looking for talented students to join our team. Requirements: Currently pursuing Computer Science degree, knowledge of Python/Java. Benefits include competitive stipend, mentorship, and potential full-time opportunities."
        },
        {
            "name": "Fake Internship with Multiple Red Flags",
            "text": "URGENT: Virtual Internship Opportunity! No experience needed. Pay $75 for completion certificate. Send your UPI ID and personal information. Quick money opportunity. Limited time offer. Anyone can apply!"
        },
        {
            "name": "Fake Internship with Certificate Cost",
            "text": "Remote Internship in Digital Marketing. Certificate cost is 2500 INR. Virtual internship with flexible timing. Pay certificate amount to get started. No qualification required."
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print("-" * 50)
        
        result, confidence_score, icon, pattern_matches = predictor.get_prediction_result(test_case['text'])
        
        print(f"Text: {test_case['text'][:80]}...")
        print(f"Result: {result}")
        print(f"Confidence Score: {confidence_score:.1f}%")
        print(f"Icon: {icon}")
        
        if pattern_matches:
            print(f"Pattern Matches Found:")
            for pattern in pattern_matches:
                print(f"  - {pattern}")
        else:
            print("No suspicious patterns detected")
        
        print()

if __name__ == "__main__":
    test_enhanced_model() 