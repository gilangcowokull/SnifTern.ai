from prediction_utils import FakeJobPredictor

def test_model():
    """Test the trained model with sample inputs"""
    print("Testing Fake Job Posting Detector Model")
    print("=" * 50)
    
    # Initialize predictor
    predictor = FakeJobPredictor()
    
    # Test cases
    test_cases = [
        {
            "name": "Real Job Posting",
            "text": "Software Engineer position at Google. We are looking for a talented software engineer to join our team. Requirements: 3+ years of experience in Python, JavaScript, and cloud technologies. Benefits include competitive salary, health insurance, and flexible work arrangements."
        },
        {
            "name": "Fake Job Posting",
            "text": "URGENT: Work from home opportunity! Make $5000 per week from your computer. No experience needed. Send us your personal information and bank details to get started immediately. This is a limited time offer!"
        },
        {
            "name": "Suspicious Job Posting",
            "text": "Data Entry Clerk - Immediate Start. We need someone to process payments and transfer funds. You will receive money in your account and send it to other accounts. Commission based. No questions asked."
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print("-" * 30)
        
        result, confidence_score, icon = predictor.get_prediction_result(test_case['text'])
        
        print(f"Text: {test_case['text'][:100]}...")
        print(f"Result: {result}")
        print(f"Confidence Score: {confidence_score:.1f}%")
        print(f"Icon: {icon}")
        print()

if __name__ == "__main__":
    test_model() 