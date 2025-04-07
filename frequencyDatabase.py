import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import json


def insert_frequencies(filename):
    # Sample data (Replace with actual scraped data)
    with open(filename, mode='r') as file:
        frequencies = json.load(file)

    # Connect to SQLite database
    conn = sqlite3.connect("/Users/dhurgadharani/Fashion/fashion_trends.db")
    cursor = conn.cursor()

    # Create a table with a timestamp to track changes over time
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fashion_trends (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL,
        frequency INTEGER NOT NULL,
        date TEXT NOT NULL   -- Store the timestamp (YYYY-MM-DD)
    )
    """)


    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get today's date
    for word, freq in frequencies.items():
        cursor.execute("INSERT INTO fashion_trends (word, frequency, date) VALUES (?, ?, ?)",
                       (word, freq, current_date))
    conn.commit()  # Save changes


    # Verify stored data
#    cursor.execute("SELECT * FROM fashion_trends")
#    rows = cursor.fetchall()

#    print("Stored Data in Database:")
#    for row in rows:
#        print(row)

    # Close the database connection
    conn.close()
    
    
def query_article_words():
    conn = sqlite3.connect("/Users/dhurgadharani/Fashion/fashion_trends.db")
    cursor = conn.cursor()

    word_to_track = "vintage"  # Change this to any word, we'll edit this later

    cursor.execute("""
    SELECT date, frequency FROM fashion_trends 
    WHERE word = ?
    ORDER BY date ASC
    """, (word_to_track,))

    trend_data = cursor.fetchall()

#    print(f"Trend for '{word_to_track}' over time:")
#    for row in trend_data:
#        print(f"Date: {row[0]}, Frequency: {row[1]}")

    conn.close()

def plot_freq_changes():
    conn = sqlite3.connect("/Users/dhurgadharani/Fashion/fashion_trends.db")
    cursor = conn.cursor()

    word_to_track = "vintage"  # Change this to any word

    cursor.execute("""
    SELECT date, frequency FROM fashion_trends 
    WHERE word = ?
    ORDER BY date ASC
    """, (word_to_track,))

    trend_data = cursor.fetchall()

    # Extract dates and frequencies for plotting
    dates = [row[0] for row in trend_data]
    frequencies = [row[1] for row in trend_data]

    # Plot the trend
    plt.figure(figsize=(10, 5))
    plt.plot(dates, frequencies, marker='o', linestyle='-', color='b', label=word_to_track)
    plt.xlabel("Date")
    plt.ylabel("Frequency")
    plt.title(f"Trend of '{word_to_track}' Over Time")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    #plt.show()
    plt.savefig("/Users/dhurgadharani/Fashion/graphs/frequencies.png", bbox_inches='tight')

    conn.close()

insert_frequencies("/Users/dhurgadharani/Fashion/data/articles_frequencies.json")
insert_frequencies("/Users/dhurgadharani/Fashion/data/caption_frequencies.json")
query_article_words()
plot_freq_changes()
