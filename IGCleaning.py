import json
import re
import string
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Path to NLTK resources bc for some reason I couldn't download them
nltk.data.path.append('path/to/nltk_data')

# Load data from JSON file
with open("data/IG_captions.json", mode='r') as file:
    dataList = json.load(file)


#Add all captions into this list
all_captions = []

for data in dataList:
    all_captions.append(data["caption"])


# Clean text function
def clean_text(text, fashion_terms):
    text = text.lower() #Changes all text to lowercase
    text = re.sub(r"http\S+|www\S+", "", text)  # Remove URLs
    text = re.sub(r"[^\w\s#]", "", text)        # Keep hashtags, remove other punctuations
    text = text.translate(str.maketrans("", "", string.punctuation)) #Create translation table to map every punctuation character to none, removing it.
    words = word_tokenize(text) #Breaks down the text into a list of words, numbers and punctuations as separate
    
    # Retrieve stopwords from NLTK library in English
    stop_words = set(stopwords.words('english'))
    
    #If the word in words is not a stop word, and is an alphabet and is in the fashion_terms list, then add it to the cleaned words list.
    cleaned_words = [
        word for word in words
        if word not in stop_words and word.isalpha() and word in fashion_terms
    
    ]
    return cleaned_words #Return the cleaned words
    
# Function to export data to JSON
def export_to_json(caption_data, filename="data/caption_frequencies.json"):
    with open(filename, mode='w') as file:
        json.dump(caption_data, file, indent=4, ensure_ascii=False)  # Write the data to the file


full_text = " ".join(all_captions) #From the JSON file, add all the captions to the same text string

fashion_terms = [
    # Fashion Items
    "dress", "shirt", "blouse", "skirt", "jeans", "pants", "shorts", "t-shirt", "sweater",
    "hoodie", "jacket", "coat", "blazer", "suit", "jumpsuit", "romper", "tunic", "cardigan",
    "vest", "sweater", "kimono", "overalls", "tracksuit", "lingerie", "socks", "leggings",
    "tights", "pajamas", "bikini", "swimwear",

    # Fashion Accessories
    "shoes", "boots", "heels", "sneakers", "flats", "sandals", "loafers", "bags", "handbag",
    "purse", "backpack", "belt", "scarf", "hat", "beanie", "cap", "sunglasses", "watch",
    "jewelry", "necklace", "earrings", "bracelets", "ring", "gloves", "cufflinks", "brooch",

    # Fashion Styles
    "casual", "formal", "business", "streetwear", "chic", "elegant", "preppy", "vintage",
    "retro", "bohemian", "boho", "minimalist", "grunge", "sporty", "glam", "glamorous", "edgy",
    "punk", "classic", "modern", "trendy", "sophisticated", "athleisure", "holiday","beach", "beachy",

    # Fashion Trends
    "fast", "sustainable", "slow", "high fashion",
    "ready-to-wear", "couture", "haute", "street", "minimalism", "upcycling",
    "eco-fashion", "smart", "gender-neutral", "techwear",

    # Fashion Fabrics and Materials
    "cotton", "denim", "silk", "wool", "leather", "velvet", "polyester", "nylon", "cashmere",
    "linen", "tweed", "fur", "satin", "lace", "chiffon", "brocade",

    # Fashion-related Concepts
    "OOTD", "style icon", "fashionista", "influencer", "fashion week", "runway", "model",
    "fashion design", "capsule wardrobe", "essentials", "fashion collection",
    "fashion magazine", "fashion photographer", "lookbook", "streetstyle"
]


# Clean words
cleaned_words = clean_text(full_text, fashion_terms)

# Word frequency
word_counts = Counter(cleaned_words)

word_frequencies = dict(word_counts)

export_to_json(word_frequencies)

# Generate Word Cloud
wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_counts)


# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
wordcloud.to_file("imgInstagram/wordcloud.png") #Save the word cloud
