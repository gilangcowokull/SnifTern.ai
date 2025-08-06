# 🔧 SnifTern.ai Integration Troubleshooting Guide

This guide helps you resolve issues with LinkedIn, Indeed, and Glassdoor integrations in your SnifTern.ai project.

## 🚨 Common Issues & Solutions

### 1. **LinkedIn Integration Not Working**

#### **Problem**: "Could not extract text from LinkedIn URL"

**Causes:**
- LinkedIn's anti-bot protection
- Invalid job posting URL
- Rate limiting
- Network connectivity issues

**Solutions:**

1. **Verify URL Format**
   ```
   ✅ Correct: https://www.linkedin.com/jobs/view/software-engineer-intern-at-google-1234567890
   ❌ Wrong: https://www.linkedin.com/company/google
   ```

2. **Use Real Job URLs**
   - Copy URLs directly from LinkedIn job postings
   - Ensure the URL contains `/jobs/view/` or `/jobs/collections/`

3. **Check Network**
   ```bash
   # Test connectivity
   curl -I https://www.linkedin.com/jobs/
   ```

4. **Update Headers** (if needed)
   ```python
   # In app.py, update LinkedIn headers
   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
       'Accept-Language': 'en-US,en;q=0.9',
       'Accept-Encoding': 'gzip, deflate, br',
       'Connection': 'keep-alive',
       'Upgrade-Insecure-Requests': '1',
       'Sec-Fetch-Dest': 'document',
       'Sec-Fetch-Mode': 'navigate',
       'Sec-Fetch-Site': 'none',
       'Cache-Control': 'max-age=0'
   }
   ```

### 2. **Indeed Integration Not Working**

#### **Problem**: "Could not extract text from Indeed URL"

**Causes:**
- Indeed's bot detection
- Invalid job URL format
- Geographic restrictions
- Rate limiting

**Solutions:**

1. **Verify URL Format**
   ```
   ✅ Correct: https://www.indeed.com/viewjob?jk=1234567890abcdef
   ✅ Correct: https://www.indeed.com/jobs?jk=1234567890abcdef
   ❌ Wrong: https://www.indeed.com/company/company-name
   ```

2. **Use Country-Specific URLs**
   ```
   US: https://www.indeed.com/viewjob?jk=...
   UK: https://uk.indeed.com/viewjob?jk=...
   CA: https://ca.indeed.com/viewjob?jk=...
   ```

3. **Add Delays**
   ```python
   # In scraping_utils.py
   import time
   import random
   
   # Add random delay between requests
   time.sleep(random.uniform(3, 6))
   ```

### 3. **Glassdoor Integration Not Working**

#### **Problem**: "Could not extract text from Glassdoor URL"

**Causes:**
- Glassdoor's anti-scraping measures
- Invalid job URL
- Login requirements
- Geographic restrictions

**Solutions:**

1. **Verify URL Format**
   ```
   ✅ Correct: https://www.glassdoor.com/Job/software-engineer-intern-jobs-SRCH_IL.0,23_KO24,50.htm
   ✅ Correct: https://www.glassdoor.com/job-listing/software-engineer-intern-1234567890
   ❌ Wrong: https://www.glassdoor.com/Overview/company-name
   ```

2. **Use Job-Specific URLs**
   - Look for URLs containing `/job-listing/` or `/Job/`
   - Avoid company overview pages

### 4. **General Integration Issues**

#### **Problem**: "Network error" or "Connection timeout"

**Solutions:**

1. **Check Internet Connection**
   ```bash
   ping google.com
   curl -I https://www.google.com
   ```

2. **Increase Timeout**
   ```python
   # In app.py, increase timeout
   response = requests.get(url, headers=headers, timeout=30)
   ```

3. **Add Retry Logic**
   ```python
   import time
   from requests.adapters import HTTPAdapter
   from requests.packages.urllib3.util.retry import Retry
   
   def create_session():
       session = requests.Session()
       retry = Retry(connect=3, backoff_factor=0.5)
       adapter = HTTPAdapter(max_retries=retry)
       session.mount('http://', adapter)
       session.mount('https://', adapter)
       return session
   ```

## 🛠️ Advanced Troubleshooting

### 1. **Debug Mode**

Enable debug logging to see what's happening:

```python
# In app.py, add logging
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# In scraping functions
logger.debug(f"Attempting to scrape: {url}")
logger.debug(f"Response status: {response.status_code}")
logger.debug(f"Response headers: {response.headers}")
```

### 2. **Test Individual Components**

```bash
# Test basic functionality
python test_integrations.py

# Test specific platform
curl -X POST http://localhost:5000/analyze_linkedin \
  -H "Content-Type: application/json" \
  -d '{"linkedin_url": "https://www.linkedin.com/jobs/view/test"}'
```

### 3. **Check Model Files**

Ensure your ML model files exist:

```bash
ls -la model/
# Should show:
# fake_job_model.pkl
# tfidf_vectorizer.pkl
```

### 4. **Verify Dependencies**

```bash
pip list | grep -E "(requests|beautifulsoup4|lxml|flask)"
```

## 🔄 Alternative Solutions

### 1. **Use Selenium (Advanced)**

If regular scraping fails, use Selenium:

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def extract_with_selenium(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        time.sleep(5)  # Wait for page to load
        content = driver.find_element_by_css_selector('.job-description').text
        return content
    finally:
        driver.quit()
```

### 2. **Use APIs (Recommended)**

Consider using official APIs when available:

```python
# LinkedIn API (requires authentication)
import linkedin.client

# Indeed API (requires API key)
import indeed.client

# Glassdoor API (requires API key)
import glassdoor.client
```

### 3. **Proxy Rotation**

If you're getting blocked:

```python
import random

proxies = [
    'http://proxy1:port',
    'http://proxy2:port',
    'http://proxy3:port'
]

proxy = random.choice(proxies)
response = requests.get(url, headers=headers, proxies={'http': proxy, 'https': proxy})
```

## 📋 Testing Checklist

Before reporting issues, verify:

- [ ] Flask app is running (`python app.py`)
- [ ] All dependencies are installed (`pip install -r requirements.txt`)
- [ ] Model files exist in `model/` directory
- [ ] Internet connection is working
- [ ] URLs are valid job posting URLs
- [ ] No firewall/antivirus blocking requests
- [ ] Using latest version of the code

## 🆘 Getting Help

If you're still having issues:

1. **Check the logs** for specific error messages
2. **Test with different URLs** from the same platform
3. **Try the test script**: `python test_integrations.py`
4. **Check if the platform is accessible** in your browser
5. **Verify your network** allows outbound HTTP requests

## 🔧 Quick Fixes

### **Immediate Solutions:**

1. **Restart the Flask app**
   ```bash
   # Stop the app (Ctrl+C)
   # Start again
   python app.py
   ```

2. **Clear browser cache** and try again

3. **Use different job URLs** from the same platform

4. **Check if the job posting is still active** (some get removed)

5. **Try the generic URL extraction** instead of platform-specific

### **If Nothing Works:**

1. **Use manual text input** - Copy and paste job descriptions manually
2. **Use the company search** feature instead
3. **Try different job platforms** (Monster, CareerBuilder, etc.)
4. **Report the issue** with specific error messages and URLs

## 📞 Support

For additional help:
- Check the main README.md file
- Review the error messages in the browser console
- Test with the provided sample data
- Ensure you're using the latest version of the code

---

**Remember**: Job platforms frequently update their websites and anti-bot measures. The scraping functions may need periodic updates to work with the latest changes. 