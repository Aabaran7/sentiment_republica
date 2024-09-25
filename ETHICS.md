
---

## Ethical Considerations in Web Scraping

Web scraping involves extracting data from websites, which raises several ethical considerations. This document outlines the primary ethical concerns associated with the Nepali Politics Sentiment Analyzer project and how I’ve addressed them.

### 1. Respecting Website Terms of Service and Robots.txt

*Action Taken:*  
Before diving into the scraping process, I carefully reviewed MyRepublica's ToS and examined their robots.txt file. I noted that the User-agent: * directive is present with an empty Disallow: line, which means all user agents are allowed to access the site. This clarity gave me the green light to proceed with scraping, knowing I was following the website's guidelines.

### 2. Rate Limiting and Server Load

*Action Taken:*  
Although I confirmed that scraping is allowed, I planned to incorporate rate limiting in my script, with delays (e.g., time.sleep(2)) between requests to avoid overwhelming MyRepublica’s servers. This step reflects my commitment to ethical scraping practices, ensuring I respect the website's resources.

### 3. Data Privacy and Confidentiality

*Action Taken:*  
I focused solely on publicly available news articles. By adhering to this principle, I avoid collecting sensitive information and ensure I’m respecting the privacy of individuals mentioned in the content.

### 4. Accurate Representation of Sentiment

*Action Taken:*  
I opted to use Google Cloud's Natural Language API for sentiment analysis, recognizing the limitations of simpler tools. With my commitment to ethical practices and the proper representation of content, I will be cautious in interpreting sentiment, ensuring users understand the potential for misinterpretation.

### 5. Purpose and Impact of Data Use

*Action Taken:*  
My goal is to provide insights for educational purposes. Since I'm moving forward with scraping MyRepublica, I remain focused on sourcing data responsibly, seeking out alternatives that align with my ethical standards and contribute positively to discussions around political sentiment in Nepal.

### Conclusion

The Nepali Politics Sentiment Analyzer project was designed with the intent to analyze sentiment from MyRepublica articles. After carefully reviewing their robots.txt and ToS, I confirmed that scraping is allowed. This decision reflects my dedication to ethical standards in data usage and respect for website policies. I’m committed to contributing meaningfully to conversations about political sentiment in Nepal through responsible data practices.

---
