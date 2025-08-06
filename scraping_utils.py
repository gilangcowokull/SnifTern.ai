import requests
from bs4 import BeautifulSoup
from preprocessing import clean_extracted_text
import time
import random

def extract_text_from_url(url):
    """
    Extract text from a webpage URL with enhanced scraping capabilities
    """
    try:
        # Enhanced headers to mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        
        # Add a small delay to be respectful
        time.sleep(random.uniform(1, 3))
        
        # Make the request with longer timeout
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script, style, and other non-content elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'iframe']):
            element.decompose()
        
        # Try to find main content area
        main_content = None
        
        # Common selectors for main content
        content_selectors = [
            'main',
            'article',
            '.main-content',
            '.content',
            '.post-content',
            '.entry-content',
            '#content',
            '#main',
            '.job-description',
            '.job-content'
        ]
        
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        # If no main content found, use body
        if not main_content:
            main_content = soup.find('body')
        
        # Extract text
        if main_content:
            text = main_content.get_text(separator=' ', strip=True)
        else:
            text = soup.get_text(separator=' ', strip=True)
        
        # Clean the extracted text
        cleaned_text = clean_extracted_text(text)
        
        return cleaned_text
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {str(e)}")
        return ""
    except Exception as e:
        print(f"Error extracting text from URL: {str(e)}")
        return ""

def is_valid_url(url):
    """
    Enhanced URL validation
    """
    try:
        if not url or not isinstance(url, str):
            return False
        
        if not url.startswith(('http://', 'https://')):
            return False
        
        # Basic URL structure validation
        if len(url) < 10:  # Too short to be a valid URL
            return False
        
        # Check for common job platform domains
        job_platforms = [
            'linkedin.com/jobs',
            'indeed.com',
            'glassdoor.com',
            'monster.com',
            'careerbuilder.com',
            'ziprecruiter.com',
            'simplyhired.com',
            'dice.com'
        ]
        
        # If it's a job platform URL, validate it's a job posting
        for platform in job_platforms:
            if platform in url:
                # For LinkedIn, ensure it's a job posting URL
                if 'linkedin.com' in url and '/jobs/' not in url:
                    return False
                return True
        
        return True
    except:
        return False

def get_platform_from_url(url):
    """
    Determine the job platform from URL
    """
    url_lower = url.lower()
    
    if 'linkedin.com/jobs' in url_lower:
        return 'linkedin'
    elif 'indeed.com' in url_lower:
        return 'indeed'
    elif 'glassdoor.com' in url_lower:
        return 'glassdoor'
    elif 'monster.com' in url_lower:
        return 'monster'
    elif 'careerbuilder.com' in url_lower:
        return 'careerbuilder'
    elif 'ziprecruiter.com' in url_lower:
        return 'ziprecruiter'
    elif 'simplyhired.com' in url_lower:
        return 'simplyhired'
    elif 'dice.com' in url_lower:
        return 'dice'
    else:
        return 'unknown'

def extract_job_content_enhanced(url):
    """
    Enhanced job content extraction with platform-specific handling
    """
    platform = get_platform_from_url(url)
    
    try:
        # Platform-specific headers
        headers = get_platform_headers(platform)
        
        # Add delay for rate limiting
        time.sleep(random.uniform(2, 4))
        
        response = requests.get(url, headers=headers, timeout=25)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Platform-specific content extraction
        if platform == 'linkedin':
            return extract_linkedin_content(soup)
        elif platform == 'indeed':
            return extract_indeed_content(soup)
        elif platform == 'glassdoor':
            return extract_glassdoor_content(soup)
        else:
            return extract_generic_content(soup)
            
    except Exception as e:
        print(f"Enhanced extraction error for {platform}: {str(e)}")
        return ""

def get_platform_headers(platform):
    """
    Get platform-specific headers
    """
    base_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }
    
    # Platform-specific headers
    if platform == 'linkedin':
        base_headers.update({
            'Referer': 'https://www.linkedin.com/',
            'Sec-Fetch-Site': 'same-origin'
        })
    elif platform == 'indeed':
        base_headers.update({
            'Referer': 'https://www.indeed.com/',
            'Sec-Fetch-Site': 'same-origin'
        })
    elif platform == 'glassdoor':
        base_headers.update({
            'Referer': 'https://www.glassdoor.com/',
            'Sec-Fetch-Site': 'same-origin'
        })
    
    return base_headers

def extract_linkedin_content(soup):
    """Extract content from LinkedIn job postings"""
    selectors = [
        '.job-description',
        '.show-more-less-html__markup',
        '.job-description__content',
        '[data-job-description]',
        '.job-description__text',
        '.description__text',
        '.job-description-content',
        '.job-description__content--rich-text'
    ]
    
    return extract_with_selectors(soup, selectors)

def extract_indeed_content(soup):
    """Extract content from Indeed job postings"""
    selectors = [
        '#jobDescriptionText',
        '.job-description',
        '[data-testid="job-description"]',
        '.jobsearch-jobDescriptionText',
        '.job-description-container',
        '.jobsearch-jobDescriptionText--container'
    ]
    
    return extract_with_selectors(soup, selectors)

def extract_glassdoor_content(soup):
    """Extract content from Glassdoor job postings"""
    selectors = [
        '.jobDescriptionContent',
        '.job-description',
        '[data-testid="job-description"]',
        '.desc',
        '.job-description-content',
        '.job-description__content'
    ]
    
    return extract_with_selectors(soup, selectors)

def extract_generic_content(soup):
    """Extract content from generic job postings"""
    selectors = [
        '.job-description',
        '.job-content',
        '.post-content',
        '.entry-content',
        '.content',
        'main',
        'article'
    ]
    
    return extract_with_selectors(soup, selectors)

def extract_with_selectors(soup, selectors):
    """Extract content using multiple selectors"""
    for selector in selectors:
        elements = soup.select(selector)
        if elements:
            text = ' '.join([elem.get_text(strip=True) for elem in elements])
            if text and len(text) > 100:  # Ensure we have substantial content
                return clean_extracted_text(text)
    
    # Fallback: try to find any substantial text content
    for element in soup(['nav', 'footer', 'header', 'script', 'style', 'aside', 'iframe']):
        element.decompose()
    
    main_content = soup.find('main') or soup.find('article') or soup.find('body')
    if main_content:
        text = main_content.get_text(strip=True)
        return clean_extracted_text(text)
    
    return "" 