import subprocess
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3
import re
import time
from google.oauth2 import service_account
from google.cloud import language_v1

num_pages = int(input("Enter the number of pages to scrape:"))

# Disable InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load Google Cloud credentials
credentials_path = 'sincere-beacon-436520-j1-284974a0cb30.json'
credentials = service_account.Credentials.from_service_account_file(
    credentials_path)

# Downloading the English model of spaCy
subprocess.check_call(
    [sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
import spacy

# Loading the English model
nlp = spacy.load("en_core_web_sm")


# Function to construct article link from the title
def construct_article_link(title):
    base_url = "https://myrepublica.nagariknetwork.com/news/"
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')
    return base_url + slug + "/"


# Function to scrape the article for content date and title
def construct_article_link(title):
    base_url = "https://myrepublica.nagariknetwork.com/news/"
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')
    return base_url + slug + "/"


# Function to scrape the article for content date and title
def scrape_politics_articles(base_url, pages):
    articles = []
    for page in range(1, pages + 1):
        url = f"{base_url}?page={page}"
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.content, 'html.parser')

        for article in soup.find_all('div', class_='main-heading'):
            title_elem = article.find('h2')
            title = title_elem.text.strip() if title_elem else 'No title'
            full_link = construct_article_link(title)

            article_response = requests.get(full_link, verify=False)
            article_soup = BeautifulSoup(article_response.content,
                                         'html.parser')

            # Extract main content from div with id="newsContent"
            content_container = article_soup.find('div', id='newsContent')

            if content_container:
                content_paragraphs = content_container.find_all('p')
                content = ' '.join([
                    p.text.strip() for p in content_paragraphs
                    if p.text.strip()
                ])
            else:
                content = 'No content'

            date_elem = article.find('p', class_='headline-time')
            date = date_elem.text.strip() if date_elem else 'No date'

            articles.append({
                'Title': title,
                'Link': full_link,
                'Date': date,
                'Content': content
            })

            time.sleep(2)

    return articles


# Function to analyze the sentiment of the article content
def analyze_sentiment(text):
    client = language_v1.LanguageServiceClient(credentials=credentials)
    document = language_v1.Document(content=text,
                                    type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    sentiment = response.document_sentiment

    if sentiment.score > 0:
        return 'Positive'
    elif sentiment.score < 0:
        return 'Negative'
    else:
        return 'Neutral'


# Base URL of myRepublica politics section
base_url = 'https://myrepublica.nagariknetwork.com/category/politics'
politics_data = scrape_politics_articles(base_url, num_pages)

# Creating a DataFrame
df = pd.DataFrame(politics_data)

# Analyze sentiment for each article's content and add it as a new column
df['Sentiment'] = df['Content'].apply(analyze_sentiment)

# List of last names to help with finding last name in the article title
last_name_list = [
    "Acharya", "Adhikari", "Agnihotri", "Agri", "Airi", "Ale", "Amast",
    "Amatya", "Amgai", "Amgain", "Angbahang", "Angraten", "Angthupuhang",
    "Ansari", "Araqi", "Arjal", "Arjyal", "Arjel", "Aryal", "Aslami",
    "Athpahare", "Awa", "Awasthi", "Bachhgoti Chauhan", "Badahi", "Badal",
    "Badi", "Bagyal", "Baijali", "Bainge", "Bajgain", "Bajyu", "Bakharel",
    "Bakhrel", "Balam", "Balami", "Bam", "Bamanayata", "Bammala", "Bania",
    "Baniya", "Banshi", "Bantar", "Bantava", "Banth", "Bantr", "Barai",
    "Baral", "Bardiya", "Barma", "Barman", "Varman", "Baruwal", "Baskota",
    "Banskota", "Basnet", "Basnyat", "Basti", "Bastola", "Basyal", "Bashyal",
    "Beduwar", "Belbase", "Benglasi", "Bha", "Bhadel", "Bhagat", "Bhandari",
    "Bhanya", "Bhat", "Bhatnagar", "Bhatta", "Bhattachan", "Bhattarai",
    "Bhetwal", "Bhetuwal", "Bhihar", "Bhotgamiya", "Bhul", "Bhool", "Bhusal",
    "Bhurtel", "Bhurtyal", "Bidari", "Bikral", "Birkatta", "Bisen",
    "Bishwokarma", "Bista", "Bisht", "Biswas", "Blon", "Bogati", "Bohra",
    "Bohara", "Boksha", "Boktan", "Bomjan", "Bote", "Brachey", "Buda", "Budha",
    "Budhaer", "Budhair", "Budhatoki", "Bura", "Burathoki", "Camkhala",
    "Chaelengarten", "Chalise", "Chamar", "Chami", "Chamlagain", "Chamlinge",
    "Chand", "Chandra", "Chapagain", "Charmakar", "Chataut", "Chaturvedi",
    "Chauden", "Chaudhari", "Chaudhary", "Chauhan", "Chaulagain", "Chaurasiya",
    "Chavey", "Chhetri", "Chhungpate", "Chidimar", "Chik", "Chitauniya",
    "Chitrakar", "Chobeguhang", "Chongbang", "Chunanra", "Churihar", "Chyame",
    "Chyamkhal", "Chyawa", "Dafali", "Dahal", "Dali", "Damai", "Damrang",
    "Dangal", "Dangauriya", "Dangi", "Dangol", "Dangora", "Danwar", "Danya",
    "Darden", "Dargarcha", "Darji", "Darjee", "Darlami", "Darnal", "Darpa",
    "Darzi", "Das", "Daubhadel", "Dawadi", "Deola", "Deppacha", "Deuba",
    "Deula", "Dev", "Devkota", "Devlinga", "Dhakal", "Dhami", "Dhandi",
    "Dhanuk", "Dharikar", "Dhankar", "Dhital", "Dhobi", "Dholi", "Dhungana",
    "Dhungel", "Dhungyal", "Dhuniya", "Dhyapa", "Dimdu", "Dixit", "Dikshit",
    "Doeja", "Dom", "Dong", "Dotel", "Dotiyal", "Dudh", "Dulal", "Durbicha",
    "Dushadh", "Duwadi", "Duwal", "Ektinhang", "Esmali", "Faqir", "Gachhadar",
    "Gaddi", "Gaha", "Gaine", "Gaire", "Gaithaula", "Gandharba", "Gandharva",
    "Garbhar", "Garden", "Garmeba", "Garshejata", "Gartola", "Gauchan",
    "Gaudel", "Gautam", "Ghale", "Ghartel", "Ghartyal", "Gharti", "G.C.",
    "Ghartmel", "Ghimire", "Ghimirya", "Ghising", "Ghodane", "Ghurcholi",
    "Ghyalang", "Gilal", "Giri", "Glan", "Gole", "Gomden", "Gonga", "Gorkhali",
    "Gotame", "Grandan", "Guragain", "Gurangain", "Gurung", "Gurwacharya",
    "Gwala", "Gyawali", "Hada", "Haeljliya", "Hajam", "Hajara", "Hajjam",
    "Halahulu", "Halal-khor", "Haldaliya", "Halkhor", "Halocha", "Haluwai",
    "Halwai", "Hamal", "Harijan", "Hellok", "Hemjliya", "Hina", "Hiski",
    "Humagain", "Hamyagain", "Hudke", "Ingbadokpa", "Jalari", "Jat", "Jauhari",
    "Jha", "Jhainti", "Jhankri", "Jhupucha", "Jijicha", "Jogi", "Jonche",
    "Joshi", "Juju", "Julaha", "Kabhuja", "Kadariya", "Kadayat", "Kadel",
    "Kaji", "Kakaihiya", "Kalar", "Kalwar", "Kalyal", "Kambang", "Kami",
    "Kamsakar", "Kandariya", "Kandel", "Kandyal", "Kanga", "Kanphata",
    "Kanphatta", "Kaphalya", "Kaphle", "Kafle", "Karanjit", "Karcholiya",
    "Karki", "Karmaba", "Karmacharya", "Karn", "Karte", "Kasain", "Kasaju",
    "Kathayat", "Katicha", "Katriya", "Katawal", "Katwal", "Katuwal", "Kawar",
    "Kayastha", "Ketra", "Kewat", "Khadayat", "Khadgi", "Khadka", "Khadga",
    "Khakurel", "Khalinge", "Khan", "Khanal", "Khand", "Khang", "Kharal",
    "Kharel", "Khas", "Khasu", "Khatave", "Khati", "Khatik", "Khatiwada",
    "Khatri", "K.C.", "Khatwe", "Khausiya", "Khawas", "Khulal", "Khunaha",
    "Khusa", "Khwakhali", "Khyargoli", "Kochila", "Koikyal", "Koirala",
    "Koiri", "Koeri", "Kori", "Kuinkel", "Kulu", "Kulunge", "Kumale",
    "Kumar Chauhan", "Kunwar", "Kurmi", "Kusle", "Laeden", "Lakaul", "Lakoul",
    "Lakhey", "Lalpuriya", "Lama", "Lamichhane", "Lampuchhwa", "Lamsal",
    "Lawat", "Lawati", "Layeku", "Lekhak", "Likhim", "Lingden", "Lo", "Lochan",
    "Lohamkami", "Lohani", "Lohar", "Lohorong", "Lopchan", "Luitel", "Luintel",
    "Mabuhang", "Madikami", "Magar", "Mahaju", "Mahant", "Mahara", "Mahapatra",
    "Maharjan", "Mahat", "Mahato", "Mainali", "Maithili", "Majhaura", "Majhi",
    "Malbariya", "Mali", "Malla", "Mallah", "Manandhar", "Mandaen", "Mandal",
    "Mangyung", "Mardaniyan", "Marhatta", "Marik", "Martu", "Marwadi",
    "Marwari", "Maske", "Maskey", "Maski", "Mathur", "Mathema", "Mayam",
    "Mayokpa", "Mestar", "Mijar", "Mishra", "Miyan", "Mochi", "Moktan",
    "Moktung", "Morangiya", "Mudbhari", "Mughal", "Mul", "Mool", "Mulepati",
    "Mulicha", "Munankarmi", "Murung", "Musa", "Musahar", "Nagarchi", "Nakami",
    "Napit", "Nat", "Natuwa", "Nepal", "Nepalya", "Neupane", "Nyaupane",
    "Ngarden", "Ngarpa", "Niraula", "Novlicha", "Nuniyar", "Od", "Ojha",
    "Ojhatanchhe", "Oli", "Ongchongbo", "Onta", "Pageni", "Pahari", "Paitola",
    "Pajunden", "Pakhrin", "Pal", "Paal", "Palikhe", "Palung", "Pandey",
    "Pandeya", "Pande", "Pandit", "Paneru", "Pangeni", "Pant", "Panthi",
    "Panthee", "Parajuli", "Parihar", "Pariyar", "Parki", "Pasi", "Paswan",
    "Pathak", "Pathan", "Patharkat", "Patra", "Patrabansh", "Paudel",
    "Paudyal", "Poudyal", "Payen", "Pegahang", "Pelmange", "Pethegimbang",
    "Phalinge", "Phanghang", "Phembu", "Phenduwa", "Phengdi", "Phewali",
    "Phungja", "Phurumbo", "Phuyal", "Piya", "Pode", "Pokhrel", "Pokharel",
    "Pradhan", "Pradhananga", "Praja", "Prajapati", "Pramuba", "Prasai",
    "Prengel", "Prihar", "Pudasaini", "Pujari", "Pulami", "Pulu", "Pun",
    "Punglang", "Punwal", "Purtel", "Putwar", "Pyakurel", "Pyakuryal",
    "Qassab", "Raghubansi", "Rahachey", "Rai", "Rajak", "Rajbaidya",
    "Rajbanshi", "Rajbhandari", "Rajhatya", "Rajhtiya", "Rajkul", "Rajlawat",
    "Rajput", "Rajopadhyaya", "Rajvamshi", "Rakaskoti", "Rakhal", "Ram",
    "Ramjoli", "Rana", "Ranabhat", "Rangrez", "Ranjitkar", "Rathaur",
    "Rathore", "Raut", "Rautar", "Ravanrajghariya", "Ravidas", "Rawal",
    "Rawat", "Raya", "Rayamajhi", "Regmi", "Rewali", "Rijal", "Rimal", "Risal",
    "Risyal", "Roka", "Rokaya", "Rokka", "Rokaha", "Rukain", "Rumba",
    "Rumdali", "Rumkhami", "Rupakheti", "Rupihang", "Saam", "Sabrey",
    "Sabzi-farosh", "Sahi", "Sahikh", "Sahukhala", "Sainju", "Saksena",
    "Saxena", "Samahang", "Samal", "Samant", "Sampange", "Sangraula",
    "Sangroula", "Sanjel", "Sapkota", "Sapu", "Sarbhang", "Sarbariya",
    "Sardar", "Sarki", "Saru", "Satihangma", "Satyal", "Sawad", "Saund",
    "Saud", "Sayyid", "Sedhai", "Sedhain", "Sen", "Shah", "Shahi", "Shakya",
    "Shamden", "Shamsher", "Shumsher", "Sharma", "Shelle", "Sherchan",
    "Sherpa", "Sherwa", "Shewan", "Shigu", "Shingden", "Shrestha",
    "Shrivastava", "Shukla", "Shyangbo", "Sidari", "Sigdel", "Sijapati",
    "Sikami", "Silwal", "Simkhara", "Singh", "Singthebe", "Sinjali",
    "Sinjapati", "Sinkhada", "Sitaula", "Siwakoti", "Solriya", "Sotange",
    "Soti", "Subba", "Subedi", "Suchikar", "Sudhi", "Sunaha", "Sunar",
    "Suryabansi", "Suwal", "Suyal", "Swangsabu", "Swansabu", "Syangtang",
    "Tabdar", "Talchabhadel", "Tamaden", "Tamang", "Tamata", "Tamchhange",
    "Tamrakar", "Tamu", "Tandukar", "Tanglami", "Tanti", "Tarali", "Tatma",
    "Tatwa", "Teli", "Tepe", "Thaiba", "Thakur", "Thakul", "Thakurai",
    "Thakurathi", "Thakuri", "Thamsuhang", "Thandar", "Thapa", "Thapalia",
    "Thapaliya", "Thatal", "Thavo", "Thebe", "Thing", "Thokur", "Thulung",
    "Thulunge", "Thumsing", "Thuppoko", "Timila", "Timilsina", "Timalsina",
    "Tirkey", "Titung", "Tiwari", "Torchaki", "Tripathi", "Tulachan",
    "Tuladhar", "Tumbahamphe", "Tumyangpa", "Tupa", "Ujjain", "Upadhyaya",
    "Upadhyay", "Upreti", "Uprety", "Vaidya", "Baidya", "Vaish", "Vajracharya",
    "Wagle", "Waiba", "Woli", "Yadav", "Yamphu", "Yongya", "Yonjan", "Yorka",
    "Zimba"
]

# Extracting last name from article title and adding to the df
df['Last_Name'] = df['Title'].apply(lambda title: next(
    (name for name in last_name_list if re.search(
        r'\b' + re.escape(name.lower()) + r'\b', title.lower())), None))


# Extract full names
def extract_full_name(content, last_name):
    if not content or not last_name:
        return None

    doc = nlp(content)
    for ent in doc.ents:
        if ent.label_ == "PERSON" and last_name.lower() in ent.text.lower():
            return ent.text
    return last_name


# Function to extract and format the date
def extract_and_format_date(raw_date):
    match = re.search(r'Published On:\s*(.+?)\s*NPT', raw_date)
    if match:
        date_str = match.group(1)
        # Map month names to numbers
        month_map = {
            'January': 1,
            'February': 2,
            'March': 3,
            'April': 4,
            'May': 5,
            'June': 6,
            'July': 7,
            'August': 8,
            'September': 9,
            'October': 10,
            'November': 11,
            'December': 12,
        }

        # Split the date string into components
        parts = date_str.split()
        month_name = parts[0]
        day = int(parts[1].rstrip(','))
        year = int(parts[2])
        time_str = ' '.join(parts[3:])

        # Create a formatted string for datetime
        formatted_datetime_str = f"{year}-{month_map[month_name]:02d}-{day:02d} {time_str}"

        # Convert to pandas datetime
        return pd.to_datetime(formatted_datetime_str,
                              format='%Y-%m-%d %I:%M %p')
    return pd.NaT  # Return Not a Time if no match


df['Full_Name'] = df.apply(
    lambda row: extract_full_name(row['Content'], row['Last_Name']), axis=1)

df['Formatted_Date'] = df['Date'].apply(extract_and_format_date)

df.replace("", pd.NA, inplace=True)  # Replace empty strings
df.fillna(value=pd.NA, inplace=True)  # Replace NaN values

# Display the results
print(df[['Title', 'Last_Name', 'Full_Name', 'Sentiment']])

# Save the DataFrame to a CSV file
df.to_csv('myrepublica_politics_articles.csv', index=False)
print(
    f"Scraped {len(df)} articles and saved to 'myrepublica_politics_articles.csv'"
)
