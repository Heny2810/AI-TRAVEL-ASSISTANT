import streamlit as st
from deep_translator import GoogleTranslator
from deep_learning import SentimentAnalyzer

# Initialize the sentiment analyzer
@st.cache_resource
def get_sentiment_analyzer():
    return SentimentAnalyzer()

# Set page config
st.set_page_config(
    page_title="AI Travel Assistant",
    page_icon="🌎",
    layout="wide"
)

# Add sidebar with app description
st.sidebar.markdown("""
# 🌎 AI Travel Assistant

Welcome to your intelligent travel companion designed to make your journey smoother and more enjoyable!

#### What We Offer:

🗣️ **Translation**
- Real-time translation
- Support for 9 major languages
- Auto-language detection

💭 **Common Phrases**
- Essential travel phrases
- Categorized by situations
- Native pronunciations

📝 **Language Exercises**
- Interactive learning
- 3 difficulty levels
- Progress tracking

🌍 **Travel Assistant**
- Destination guides
- Budget planning
- Travel tips

❤️ **Reviews**
- Sentiment analysis
- Rating system
- Travel feedback

---
*Made with ❤️ by Team AI Travel Assistant*
""")

# Title with icon
st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px;">
        <img src="https://em-content.zobj.net/source/microsoft-teams/363/globe-showing-americas_1f30e.png" width="50">
        <h1 style="margin: 0;">Travel Buddy</h1>
        <span style="color: #666; font-size: 1.2em; margin-left: 10px;">(AI Travel Assistant)</span>
    </div>
    """, unsafe_allow_html=True)

# Common phrases dictionary
COMMON_PHRASES = {
    "Greetings": {
        "spanish": ["¡Hola! (Hello)", "¡Buenos días! (Good morning)", "¡Buenas tardes! (Good afternoon)", "¡Buenas noches! (Good night)", "¡Hasta luego! (See you later)", "¡Adiós! (Goodbye)", "¡Gracias! (Thank you)", "Por favor (Please)", "De nada (You're welcome)"],
        "french": ["Bonjour! (Hello)", "Bon matin! (Good morning)", "Bonsoir! (Good evening)", "Bonne nuit! (Good night)", "Au revoir! (Goodbye)", "Merci! (Thank you)", "S'il vous plaît (Please)", "De rien (You're welcome)", "À bientôt! (See you soon)"],
        "german": ["Hallo! (Hello)", "Guten Morgen! (Good morning)", "Guten Tag! (Good day)", "Gute Nacht! (Good night)", "Auf Wiedersehen! (Goodbye)", "Danke! (Thank you)", "Bitte (Please)", "Bitte schön (You're welcome)", "Bis später! (See you later)"],
        "italian": ["Ciao! (Hello)", "Buongiorno! (Good morning)", "Buonasera! (Good evening)", "Buonanotte! (Good night)", "Arrivederci! (Goodbye)", "Grazie! (Thank you)", "Per favore (Please)", "Prego (You're welcome)", "A presto! (See you soon)"],
        "portuguese": ["Olá! (Hello)", "Bom dia! (Good morning)", "Boa tarde! (Good afternoon)", "Boa noite! (Good night)", "Adeus! (Goodbye)", "Obrigado/a! (Thank you)", "Por favor (Please)", "De nada (You're welcome)", "Até logo! (See you later)"],
        "japanese": ["こんにちは! (Konnichiwa - Hello)", "おはようございます! (Ohayou gozaimasu - Good morning)", "こんばんは! (Konbanwa - Good evening)", "さようなら! (Sayounara - Goodbye)", "ありがとうございます! (Arigatou gozaimasu - Thank you)", "お願いします (Onegaishimasu - Please)", "どういたしまして (Douitashimashite - You're welcome)"]
    },
    "Directions": {
        "spanish": ["¿Dónde está...? (Where is...?)", "A la derecha (To the right)", "A la izquierda (To the left)", "Todo recto (Straight ahead)", "Cerca de (Near to)", "Lejos de (Far from)", "¿Cómo llego a...? (How do I get to...?)", "La estación (The station)", "El aeropuerto (The airport)"],
        "french": ["Où est...? (Where is...?)", "À droite (To the right)", "À gauche (To the left)", "Tout droit (Straight ahead)", "Près de (Near to)", "Loin de (Far from)", "Comment aller à...? (How to get to...?)", "La gare (The station)", "L'aéroport (The airport)"],
        "german": ["Wo ist...? (Where is...?)", "Nach rechts (To the right)", "Nach links (To the left)", "Geradeaus (Straight ahead)", "In der Nähe von (Near to)", "Weit von (Far from)", "Wie komme ich zu...? (How do I get to...?)", "Der Bahnhof (The station)", "Der Flughafen (The airport)"],
        "italian": ["Dov'è...? (Where is...?)", "A destra (To the right)", "A sinistra (To the left)", "Dritto (Straight ahead)", "Vicino a (Near to)", "Lontano da (Far from)", "Come arrivo a...? (How do I get to...?)", "La stazione (The station)", "L'aeroporto (The airport)"],
        "portuguese": ["Onde está...? (Where is...?)", "À direita (To the right)", "À esquerda (To the left)", "Em frente (Straight ahead)", "Perto de (Near to)", "Longe de (Far from)", "Como chego a...? (How do I get to...?)", "A estação (The station)", "O aeroporto (The airport)"],
        "japanese": ["...はどこですか? (...wa doko desu ka? - Where is...?)", "右 (Migi - Right)", "左 (Hidari - Left)", "まっすぐ (Massugu - Straight ahead)", "近く (Chikaku - Near)", "遠く (Tooku - Far)", "...への行き方 (...he no ikikata - How to get to...?)", "駅 (Eki - Station)", "空港 (Kuukou - Airport)"]
    },
    "Emergency": {
        "spanish": ["¡Ayuda! (Help!)", "¿Dónde está el hospital? (Where is the hospital?)", "Necesito un médico (I need a doctor)", "¡Llame a la policía! (Call the police!)", "¡Es una emergencia! (It's an emergency!)", "Me he perdido (I'm lost)", "Estoy enfermo/a (I'm sick)"],
        "french": ["Au secours! (Help!)", "Où est l'hôpital? (Where is the hospital?)", "J'ai besoin d'un médecin (I need a doctor)", "Appelez la police! (Call the police!)", "C'est une urgence! (It's an emergency!)", "Je suis perdu(e) (I'm lost)", "Je suis malade (I'm sick)"],
        "german": ["Hilfe! (Help!)", "Wo ist das Krankenhaus? (Where is the hospital?)", "Ich brauche einen Arzt (I need a doctor)", "Rufen Sie die Polizei! (Call the police!)", "Es ist ein Notfall! (It's an emergency!)", "Ich habe mich verlaufen (I'm lost)", "Ich bin krank (I'm sick)"],
        "italian": ["Aiuto! (Help!)", "Dov'è l'ospedale? (Where is the hospital?)", "Ho bisogno di un medico (I need a doctor)", "Chiami la polizia! (Call the police!)", "È un'emergenza! (It's an emergency!)", "Mi sono perso/a (I'm lost)", "Sono malato/a (I'm sick)"],
        "portuguese": ["Socorro! (Help!)", "Onde fica o hospital? (Where is the hospital?)", "Preciso de um médico (I need a doctor)", "Chame a polícia! (Call the police!)", "É uma emergência! (It's an emergency!)", "Estou perdido/a (I'm lost)", "Estou doente (I'm sick)"],
        "japanese": ["助けて! (Tasukete! - Help!)", "病院はどこですか? (Byouin wa doko desu ka? - Where is the hospital?)", "医者が必要です (Isha ga hitsuyou desu - I need a doctor)", "警察を呼んでください! (Keisatsu wo yonde kudasai! - Call the police!)", "緊急事態です! (Kinkyuu jitai desu! - It's an emergency!)", "迷子です (Maigo desu - I'm lost)", "病気です (Byouki desu - I'm sick)"]
    },
    "Restaurant & Food": {
        "spanish": ["La cuenta, por favor (The bill, please)", "Una mesa para dos (A table for two)", "El menú, por favor (The menu, please)", "¡Buen provecho! (Enjoy your meal!)", "Está delicioso (It's delicious)", "Soy vegetariano/a (I'm vegetarian)", "Soy alérgico/a a... (I'm allergic to...)", "Agua (Water)", "Vino (Wine)"],
        "french": ["L'addition, s'il vous plaît (The bill, please)", "Une table pour deux (A table for two)", "Le menu, s'il vous plaît (The menu, please)", "Bon appétit! (Enjoy your meal!)", "C'est délicieux (It's delicious)", "Je suis végétarien/ne (I'm vegetarian)", "Je suis allergique à... (I'm allergic to...)", "Eau (Water)", "Vin (Wine)"],
        "german": ["Die Rechnung, bitte (The bill, please)", "Einen Tisch für zwei (A table for two)", "Die Speisekarte, bitte (The menu, please)", "Guten Appetit! (Enjoy your meal!)", "Es ist köstlich (It's delicious)", "Ich bin Vegetarier/in (I'm vegetarian)", "Ich bin allergisch gegen... (I'm allergic to...)", "Wasser (Water)", "Wein (Wine)"],
        "italian": ["Il conto, per favore (The bill, please)", "Un tavolo per due (A table for two)", "Il menu, per favore (The menu, please)", "Buon appetito! (Enjoy your meal!)", "È delizioso (It's delicious)", "Sono vegetariano/a (I'm vegetarian)", "Sono allergico/a a... (I'm allergic to...)", "Acqua (Water)", "Vino (Wine)"],
        "portuguese": ["A conta, por favor (The bill, please)", "Uma mesa para dois (A table for two)", "O cardápio, por favor (The menu, please)", "Bom apetite! (Enjoy your meal!)", "Está delicioso (It's delicious)", "Sou vegetariano/a (I'm vegetarian)", "Sou alérgico/a a... (I'm allergic to...)", "Água (Water)", "Vinho (Wine)"],
        "japanese": ["お会計お願いします (Okaikei onegaishimasu - The bill, please)", "二人席をお願いします (Futariseki wo onegaishimasu - A table for two)", "メニューをお願いします (Menyuu wo onegaishimasu - The menu, please)", "いただきます (Itadakimasu - Enjoy your meal!)", "美味しいです (Oishii desu - It's delicious)", "ベジタリアンです (Bejitarian desu - I'm vegetarian)", "アレルギーがあります (Arerugii ga arimasu - I have allergies)", "水 (Mizu - Water)", "ワイン (Wain - Wine)"]
    },
    "Shopping & Numbers": {
        "spanish": ["¿Cuánto cuesta? (How much is it?)", "Es demasiado caro (It's too expensive)", "¡Está en oferta! (It's on sale!)", "Uno, dos, tres (One, two, three)", "Diez, veinte, treinta (Ten, twenty, thirty)", "Cien, mil (Hundred, thousand)", "Efectivo (Cash)", "Tarjeta de crédito (Credit card)"],
        "french": ["Combien ça coûte? (How much is it?)", "C'est trop cher (It's too expensive)", "C'est en solde! (It's on sale!)", "Un, deux, trois (One, two, three)", "Dix, vingt, trente (Ten, twenty, thirty)", "Cent, mille (Hundred, thousand)", "Espèces (Cash)", "Carte de crédit (Credit card)"],
        "german": ["Wie viel kostet das? (How much is it?)", "Das ist zu teuer (It's too expensive)", "Das ist im Angebot! (It's on sale!)", "Eins, zwei, drei (One, two, three)", "Zehn, zwanzig, dreißig (Ten, twenty, thirty)", "Hundert, tausend (Hundred, thousand)", "Bargeld (Cash)", "Kreditkarte (Credit card)"],
        "italian": ["Quanto costa? (How much is it?)", "È troppo caro (It's too expensive)", "È in offerta! (It's on sale!)", "Uno, due, tre (One, two, three)", "Dieci, venti, trenta (Ten, twenty, thirty)", "Cento, mille (Hundred, thousand)", "Contanti (Cash)", "Carta di credito (Credit card)"],
        "portuguese": ["Quanto custa? (How much is it?)", "É muito caro (It's too expensive)", "Está em promoção! (It's on sale!)", "Um, dois, três (One, two, three)", "Dez, vinte, trinta (Ten, twenty, thirty)", "Cem, mil (Hundred, thousand)", "Dinheiro (Cash)", "Cartão de crédito (Credit card)"],
        "japanese": ["いくらですか? (Ikura desu ka? - How much is it?)", "高すぎます (Takasugimasu - It's too expensive)", "セール中です! (Seeru-chuu desu! - It's on sale!)", "一、二、三 (Ichi, ni, san - One, two, three)", "十、二十、三十 (Juu, nijuu, sanjuu - Ten, twenty, thirty)", "百、千 (Hyaku, sen - Hundred, thousand)", "現金 (Genkin - Cash)", "クレジットカード (Kurejitto kaado - Credit card)"]
    }
}

# Language exercises
EXERCISES = {
    "Basic": {
        "spanish": [
            {"question": "What is 'hello' in Spanish?", "answer": "hola"},
            {"question": "What is 'thank you' in Spanish?", "answer": "gracias"},
            {"question": "What is 'yes' in Spanish?", "answer": "sí"},
            {"question": "What is 'no' in Spanish?", "answer": "no"}
        ],
        "french": [
            {"question": "What is 'hello' in French?", "answer": "bonjour"},
            {"question": "What is 'thank you' in French?", "answer": "merci"},
            {"question": "What is 'yes' in French?", "answer": "oui"},
            {"question": "What is 'no' in French?", "answer": "non"}
        ],
        "german": [
            {"question": "What is 'hello' in German?", "answer": "hallo"},
            {"question": "What is 'thank you' in German?", "answer": "danke"},
            {"question": "What is 'yes' in German?", "answer": "ja"},
            {"question": "What is 'no' in German?", "answer": "nein"}
        ],
        "italian": [
            {"question": "What is 'hello' in Italian?", "answer": "ciao"},
            {"question": "What is 'thank you' in Italian?", "answer": "grazie"},
            {"question": "What is 'yes' in Italian?", "answer": "si"},
            {"question": "What is 'no' in Italian?", "answer": "no"}
        ],
        "portuguese": [
            {"question": "What is 'hello' in Portuguese?", "answer": "ola"},
            {"question": "What is 'thank you' in Portuguese?", "answer": "obrigado"},
            {"question": "What is 'yes' in Portuguese?", "answer": "sim"},
            {"question": "What is 'no' in Portuguese?", "answer": "nao"}
        ],
        "japanese": [
            {"question": "What is 'hello' in Japanese?", "answer": "konnichiwa"},
            {"question": "What is 'thank you' in Japanese?", "answer": "arigatou"},
            {"question": "What is 'yes' in Japanese?", "answer": "hai"},
            {"question": "What is 'no' in Japanese?", "answer": "iie"}
        ]
    },
    "Intermediate": {
        "spanish": [
            {"question": "How do you say 'How are you?' in Spanish?", "answer": "como estas"},
            {"question": "What is 'good morning' in Spanish?", "answer": "buenos dias"},
            {"question": "How do you say 'please' in Spanish?", "answer": "por favor"},
            {"question": "What is 'excuse me' in Spanish?", "answer": "perdon"}
        ],
        "french": [
            {"question": "How do you say 'How are you?' in French?", "answer": "comment allez vous"},
            {"question": "What is 'good morning' in French?", "answer": "bonjour"},
            {"question": "How do you say 'please' in French?", "answer": "s'il vous plait"},
            {"question": "What is 'excuse me' in French?", "answer": "excusez moi"}
        ],
        "german": [
            {"question": "How do you say 'How are you?' in German?", "answer": "wie geht es dir"},
            {"question": "What is 'good morning' in German?", "answer": "guten morgen"},
            {"question": "How do you say 'please' in German?", "answer": "bitte"},
            {"question": "What is 'excuse me' in German?", "answer": "entschuldigung"}
        ],
        "italian": [
            {"question": "How do you say 'How are you?' in Italian?", "answer": "come stai"},
            {"question": "What is 'good morning' in Italian?", "answer": "buongiorno"},
            {"question": "How do you say 'please' in Italian?", "answer": "per favore"},
            {"question": "What is 'excuse me' in Italian?", "answer": "scusi"}
        ],
        "portuguese": [
            {"question": "How do you say 'How are you?' in Portuguese?", "answer": "como esta"},
            {"question": "What is 'good morning' in Portuguese?", "answer": "bom dia"},
            {"question": "How do you say 'please' in Portuguese?", "answer": "por favor"},
            {"question": "What is 'excuse me' in Portuguese?", "answer": "com licenca"}
        ],
        "japanese": [
            {"question": "How do you say 'How are you?' in Japanese?", "answer": "ogenki desu ka"},
            {"question": "What is 'good morning' in Japanese?", "answer": "ohayou gozaimasu"},
            {"question": "How do you say 'please' in Japanese?", "answer": "onegaishimasu"},
            {"question": "What is 'excuse me' in Japanese?", "answer": "sumimasen"}
        ]
    },
    "Advanced": {
        "spanish": [
            {"question": "Translate 'I would like to order food' to Spanish", "answer": "quisiera pedir comida"},
            {"question": "How do you say 'Could you help me find the hotel?' in Spanish?", "answer": "podria ayudarme a encontrar el hotel"},
            {"question": "Translate 'I don't understand, could you speak slower?' to Spanish", "answer": "no entiendo, podria hablar mas despacio"},
            {"question": "How do you say 'What time does the museum open?' in Spanish?", "answer": "a que hora abre el museo"}
        ],
        "french": [
            {"question": "Translate 'I would like to order food' to French", "answer": "je voudrais commander a manger"},
            {"question": "How do you say 'Could you help me find the hotel?' in French?", "answer": "pourriez vous m'aider a trouver l'hotel"},
            {"question": "Translate 'I don't understand, could you speak slower?' to French", "answer": "je ne comprends pas, pourriez vous parler plus lentement"},
            {"question": "How do you say 'What time does the museum open?' in French?", "answer": "a quelle heure ouvre le musee"}
        ],
        "german": [
            {"question": "Translate 'I would like to order food' to German", "answer": "ich mochte essen bestellen"},
            {"question": "How do you say 'Could you help me find the hotel?' in German?", "answer": "konnten sie mir helfen das hotel zu finden"},
            {"question": "Translate 'I don't understand, could you speak slower?' to German", "answer": "ich verstehe nicht, konnten sie langsamer sprechen"},
            {"question": "How do you say 'What time does the museum open?' in German?", "answer": "wann offnet das museum"}
        ],
        "italian": [
            {"question": "Translate 'I would like to order food' to Italian", "answer": "vorrei ordinare da mangiare"},
            {"question": "How do you say 'Could you help me find the hotel?' in Italian?", "answer": "potrebbe aiutarmi a trovare l'hotel"},
            {"question": "Translate 'I don't understand, could you speak slower?' to Italian", "answer": "non capisco, potrebbe parlare piu lentamente"},
            {"question": "How do you say 'What time does the museum open?' in Italian?", "answer": "a che ora apre il museo"}
        ],
        "portuguese": [
            {"question": "Translate 'I would like to order food' to Portuguese", "answer": "eu gostaria de pedir comida"},
            {"question": "How do you say 'Could you help me find the hotel?' in Portuguese?", "answer": "poderia me ajudar a encontrar o hotel"},
            {"question": "Translate 'I don't understand, could you speak slower?' to Portuguese", "answer": "nao entendo, poderia falar mais devagar"},
            {"question": "How do you say 'What time does the museum open?' in Portuguese?", "answer": "que horas o museu abre"}
        ],
        "japanese": [
            {"question": "Translate 'I would like to order food' to Japanese", "answer": "tabemono wo chuumon shitai desu"},
            {"question": "How do you say 'Could you help me find the hotel?' in Japanese?", "answer": "hoteru wo sagasu no wo tetsudatte itadakemasu ka"},
            {"question": "Translate 'I don't understand, could you speak slower?' to Japanese", "answer": "wakarimasen yukkuri hanashite kudasai"},
            {"question": "How do you say 'What time does the museum open?' in Japanese?", "answer": "hakubutsukan wa nanji ni akimasu ka"}
        ]
    }
}

def analyze_sentiment(text):
    """Analyze sentiment using BERT with enhanced confidence"""
    analyzer = get_sentiment_analyzer()
    # Get basic sentiment analysis
    result = analyzer.analyze(text, include_aspects=True)  # Enable aspect analysis
    
    # Enhance confidence for short, clear reviews
    confidence = result['confidence'] * 100
    
    # Boost confidence for clear sentiment indicators
    clear_positive = ['amazing', 'excellent', 'great', 'wonderful', 'fantastic', 'perfect']
    clear_negative = ['terrible', 'horrible', 'awful', 'poor', 'bad', 'worst']
    
    words = text.lower().split()
    if any(word in words for word in clear_positive + clear_negative):
        confidence = min(confidence * 1.2, 100)  # Boost confidence but cap at 100%
    
    # If aspects are analyzed and consistent, boost confidence
    if 'aspects' in result and result['aspects']:
        aspect_sentiments = [details['score'] for details in result['aspects'].values()]
        if all(s >= 4 for s in aspect_sentiments) or all(s <= 2 for s in aspect_sentiments):
            confidence = min(confidence * 1.1, 100)  # Boost confidence for consistent aspects
    
    return {
        'label': result['sentiment'],
        'score': result['score'],
        'confidence': confidence,
        'aspects': result.get('aspects', {})
    }

# Predefined travel-related responses
TRAVEL_RESPONSES = {
    "weather": "For accurate weather information, I recommend checking local weather services or apps for your specific destination.",
    "packing": "Here's a basic packing checklist:\n- Passport/ID\n- Clothing appropriate for the climate\n- Toiletries\n- Medications\n- Electronics & chargers\n- Travel documents\n- Local currency",
    "safety": "General travel safety tips:\n- Keep important documents secure\n- Stay aware of your surroundings\n- Keep emergency contacts handy\n- Research local customs and areas to avoid\n- Have travel insurance",
    "budget": "To plan your budget:\n- Research accommodation costs\n- Plan for daily meals\n- Include transportation expenses\n- Account for activities and attractions\n- Keep emergency funds\n- Consider local currency exchange rates",
    "transportation": "Common transportation options:\n- Public transit (buses, trains)\n- Taxis/ride-sharing\n- Car rentals\n- Walking/cycling for local exploration\n- Airport transfers",
    "accommodation": "Accommodation tips:\n- Book in advance for better rates\n- Read recent reviews\n- Check location and accessibility\n- Verify amenities included\n- Consider local alternatives to hotels",
    "culture": "Cultural preparation tips:\n- Learn basic local phrases\n- Research customs and etiquette\n- Respect local dress codes\n- Be aware of cultural sensitivities\n- Try local cuisine",
    "newzealand": "Travel to New Zealand typically requires:\n- At least $1000-1500 for basic accommodations\n- $500-700 for local transportation\n- $400-500 for food and activities\n- Additional costs for flights ($800-2000)\n- Valid passport and visa\n\nUnfortunately, $200 would not be enough for a trip to New Zealand. The minimum recommended budget is around $3000-4000 for a basic 1-week trip, including flights.\n\nSome alternatives you might consider:\n1. Save more money before planning the trip\n2. Look for working holiday opportunities\n3. Consider closer destinations with lower costs\n4. Watch for flight deals and off-season discounts",
    "cheap": "Tips for budget travel:\n1. Travel during off-season\n2. Book flights in advance\n3. Stay in hostels or use Couchsurfing\n4. Cook your own meals\n5. Use public transportation\n6. Look for free activities and attractions\n7. Consider less expensive destinations\n8. Join travel rewards programs\n9. Use flight deal alerts\n10. Travel to countries with lower cost of living"
}

# Predefined travel-related responses
DESTINATIONS = {
    "france": {
        "famous_places": """Famous destinations in France:
1. Paris
   - Eiffel Tower
   - Louvre Museum
   - Notre-Dame Cathedral
   - Champs-Élysées
   - Palace of Versailles

2. French Riviera
   - Nice
   - Cannes
   - Saint-Tropez
   - Monaco

3. Loire Valley
   - Famous for châteaux
   - Wine regions
   - Historic towns

4. Mont Saint-Michel
   - UNESCO World Heritage site
   - Medieval monastery
   - Unique tidal island

5. French Alps
   - Chamonix
   - Mont Blanc
   - World-class skiing

Best time to visit: Spring (April-June) or Fall (September-October)
Peak tourist season: Summer (July-August)
""",
        "budget": """Estimated costs for France:
- Budget travel: €70-100 per day
- Mid-range: €150-250 per day
- Luxury: €300+ per day

Breakdown:
- Hostels: €25-40/night
- Mid-range hotels: €100-200/night
- Meals: €15-40 per meal
- Transportation: €5-15 per day (public transit)
- Museum passes: €15-20 per museum
""",
        "tips": """Travel tips for France:
1. Learn basic French phrases
2. Book major attractions in advance
3. Many shops close on Sundays
4. Tipping is not required (service included)
5. Get a Museum Pass for Paris
6. Use the efficient train system
7. Watch for pickpockets in tourist areas
8. Restaurants serve lunch 12-2 and dinner 7:30-10:30"""
    },
    "italy": {
        "famous_places": """Famous destinations in Italy:
1. Rome
   - Colosseum
   - Vatican City
   - Roman Forum
   - Trevi Fountain

2. Venice
   - St. Mark's Square
   - Grand Canal
   - Rialto Bridge

3. Florence
   - Uffizi Gallery
   - Duomo
   - Ponte Vecchio

4. Tuscany
   - Wine regions
   - Medieval towns
   - Rolling hills

5. Amalfi Coast
   - Positano
   - Capri
   - Scenic drives""",
        "budget": """Estimated costs for Italy:
- Budget travel: €60-90 per day
- Mid-range: €120-200 per day
- Luxury: €250+ per day

Breakdown:
- Hostels: €20-35/night
- Mid-range hotels: €80-150/night
- Meals: €10-30 per meal
- Transportation: €5-15 per day
- Museum entries: €10-20 each"""
    },
    "japan": {
        "famous_places": """Famous destinations in Japan:
1. Tokyo
   - Shibuya Crossing
   - Senso-ji Temple
   - Tokyo Skytree
   - Akihabara

2. Kyoto
   - Fushimi Inari Shrine
   - Kinkaku-ji
   - Arashiyama Bamboo Grove

3. Mount Fuji
   - Hiking trails
   - Five Lakes region
   - Hot springs

4. Osaka
   - Osaka Castle
   - Dotonbori
   - Universal Studios

5. Hiroshima
   - Peace Memorial
   - Miyajima Island""",
        "budget": """Estimated costs for Japan:
- Budget travel: ¥8,000-12,000 per day
- Mid-range: ¥15,000-25,000 per day
- Luxury: ¥30,000+ per day

Breakdown:
- Hostels: ¥3,000-4,000/night
- Mid-range hotels: ¥10,000-20,000/night
- Meals: ¥600-1,500 per meal
- JR Pass: ¥29,650 for 7 days
- Temple/shrine entry: ¥300-1,000"""
    }
}

def get_travel_response(user_input):
    """Generate more specific travel responses based on user input"""
    user_input_lower = user_input.lower()
    
    # Check for destination-specific questions
    for destination in DESTINATIONS.keys():
        if destination in user_input_lower:
            if "famous" in user_input_lower or "place" in user_input_lower or "destination" in user_input_lower:
                return DESTINATIONS[destination]["famous_places"]
            elif "budget" in user_input_lower or "cost" in user_input_lower or "money" in user_input_lower:
                return DESTINATIONS[destination]["budget"]
            elif "tip" in user_input_lower or "advice" in user_input_lower:
                return DESTINATIONS[destination].get("tips", "Travel tips coming soon for this destination!")
    
    # Check for specific budget questions about New Zealand
    if "enough" in user_input_lower and any(place in user_input_lower for place in ["newzealand", "new zealand"]):
        return TRAVEL_RESPONSES["newzealand"]
    
    # Check for budget travel questions
    if any(word in user_input_lower for word in ["cheap", "budget", "affordable", "save money"]):
        return TRAVEL_RESPONSES["cheap"]
    
    # Check for weather-related questions
    if "weather" in user_input_lower:
        return TRAVEL_RESPONSES["weather"]
    
    # Check for packing questions
    if "pack" in user_input_lower or "bring" in user_input_lower:
        return TRAVEL_RESPONSES["packing"]
    
    # Check for safety questions
    if "safe" in user_input_lower or "security" in user_input_lower:
        return TRAVEL_RESPONSES["safety"]
    
    # Check for transportation questions
    if any(word in user_input_lower for word in ["transport", "travel", "get around", "bus", "train"]):
        return TRAVEL_RESPONSES["transportation"]
    
    # Check for accommodation questions
    if any(word in user_input_lower for word in ["hotel", "stay", "hostel", "accommodation", "airbnb"]):
        return TRAVEL_RESPONSES["accommodation"]
    
    # Check for cultural questions
    if any(word in user_input_lower for word in ["culture", "custom", "tradition", "etiquette"]):
        return TRAVEL_RESPONSES["culture"]
    
    # Default response with helpful suggestions
    return """I can help you with specific information about:

1. Popular destinations:
   - France
   - Italy
   - Japan
   - New Zealand
   (More coming soon!)

2. Travel topics:
   - Budget and costs
   - Famous places
   - Local transportation
   - Accommodation
   - Safety tips
   - Cultural customs
   - Packing advice
   - Weather information

Try asking questions like:
- "What are famous places in France?"
- "How much does it cost to visit Japan?"
- "What's the best way to get around in Italy?"
- "What should I pack for my trip?"
"""

def main():
    # Initialize session state for current page if not exists
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Translation"

    # Title with icon
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
            <img src="https://em-content.zobj.net/source/microsoft-teams/363/globe-showing-americas_1f30e.png" width="50">
            <h1 style="margin: 0; color: #333;">AI Travel Assistant</h1>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation buttons
    cols = st.columns(5)
    with cols[0]:
        if st.button("🗣️ Translation", type="primary" if st.session_state.current_page == "Translation" else "secondary"):
            st.session_state.current_page = "Translation"
    with cols[1]:
        if st.button("💭 Phrases", type="primary" if st.session_state.current_page == "Phrases" else "secondary"):
            st.session_state.current_page = "Phrases"
    with cols[2]:
        if st.button("📝 Exercises", type="primary" if st.session_state.current_page == "Exercises" else "secondary"):
            st.session_state.current_page = "Exercises"
    with cols[3]:
        if st.button("🌍 Assistant", type="primary" if st.session_state.current_page == "Assistant" else "secondary"):
            st.session_state.current_page = "Assistant"
    with cols[4]:
        if st.button("❤️ Reviews", type="primary" if st.session_state.current_page == "Reviews" else "secondary"):
            st.session_state.current_page = "Reviews"
    
    st.markdown("---")

    # Page content
    if st.session_state.current_page == "Translation":
        st.title("Language Translation")
        col1, col2 = st.columns(2)
        with col1:
            source_lang = st.selectbox(
                "Translate from:",
                ["auto", "english", "spanish", "french", "german", "italian", "portuguese", "chinese", "japanese", "korean"]
            )
        with col2:
            target_lang = st.selectbox(
                "Translate to:",
                ["english", "spanish", "french", "german", "italian", "portuguese", "chinese", "japanese", "korean"]
            )
        text = st.text_area("Enter text to translate:", height=150)
        if st.button("Translate", type="primary") and text:
            try:
                translator = GoogleTranslator(source=source_lang, target=target_lang)
                result = translator.translate(text)
                st.success(result)
            except Exception as e:
                st.error("Translation failed. Please try again.")

    elif st.session_state.current_page == "Phrases":
        st.title("Common Travel Phrases")
        # Get all available languages from the first category
        available_languages = list(COMMON_PHRASES["Greetings"].keys())
        language = st.selectbox(
            "Select language:",
            available_languages,
            format_func=lambda x: x.title()  # Capitalize language names
        ).lower()
        
        category = st.selectbox(
            "Choose category:",
            list(COMMON_PHRASES.keys())
        )
        
        if language and category:
            st.markdown(f"### Essential {category} in {language.title()}")
            for phrase in COMMON_PHRASES[category][language]:
                st.markdown(f"• {phrase}")

    elif st.session_state.current_page == "Exercises":
        st.title("Language Exercises")
        # Get all available languages from exercises
        available_languages = list(EXERCISES["Basic"].keys())
        language = st.selectbox(
            "Select language:",
            available_languages,
            format_func=lambda x: x.title()
        ).lower()
        
        exercise_type = st.selectbox(
            "Choose difficulty level:",
            list(EXERCISES.keys()),
            help="Basic: Simple words and greetings\nIntermediate: Common phrases and questions\nAdvanced: Complex sentences and conversations"
        )
        
        if language and exercise_type:
            st.markdown(f"### {exercise_type} Level Exercise")
            
            # Initialize score
            correct_answers = 0
            total_questions = len(EXERCISES[exercise_type][language])
            
            # Create a form for all questions
            with st.form("exercise_form"):
                for idx, exercise in enumerate(EXERCISES[exercise_type][language], 1):
                    st.markdown(f"**Question {idx}:** {exercise['question']}")
                    answer = st.text_input(f"Your answer {idx}", key=f"exercise_{idx}")
                    
                    # Check answer without showing result yet
                    if answer.lower().strip() == exercise['answer'].lower():
                        correct_answers += 1
                
                # Submit button for all answers
                submitted = st.form_submit_button("Check Answers", type="primary")
                
                if submitted:
                    score_percentage = (correct_answers / total_questions) * 100
                    
                    # Show score with appropriate color and message
                    st.markdown("### Your Results:")
                    score_color = "green" if score_percentage >= 75 else "orange" if score_percentage >= 50 else "red"
                    st.markdown(f"<h2 style='color: {score_color}'>Score: {score_percentage:.1f}%</h2>", unsafe_allow_html=True)
                    st.markdown(f"**Correct Answers:** {correct_answers} out of {total_questions}")
                    
                    # Show encouraging message based on score
                    if score_percentage == 100:
                        st.success("🎉 Perfect score! You're ready for the next level!")
                    elif score_percentage >= 75:
                        st.success("🌟 Great job! Keep practicing to perfect your skills!")
                    elif score_percentage >= 50:
                        st.warning("👍 Good effort! Review the answers and try again!")
                    else:
                        st.error("📚 Keep practicing! Try an easier level or review the phrases section!")
                    
                    # Show correct answers
                    st.markdown("### Review:")
                    for exercise in EXERCISES[exercise_type][language]:
                        st.markdown(f"**Q:** {exercise['question']}")
                        st.markdown(f"**A:** {exercise['answer']}")
                        st.markdown("---")

    elif st.session_state.current_page == "Reviews":
        st.title("Travel Review Analysis")
        
        # Input section
        review_text = st.text_area(
            "Enter your travel review:",
            height=150,
            placeholder="Example: The hotel was amazing with great views. The staff was very friendly and helpful."
        )

        # Sample reviews
        if st.checkbox("Show sample reviews"):
            samples = {
                "Positive Review": "The hotel was amazing! Great views, friendly staff, and delicious breakfast.",
                "Mixed Review": "Nice location and clean rooms, but the service was slow.",
                "Negative Review": "Poor experience. Long delays, unfriendly staff, and overpriced."
            }
            selected = st.selectbox("Choose a sample:", list(samples.keys()))
            if selected:
                review_text = samples[selected]

        # Analysis button
        if st.button("Analyze", type="primary") and review_text:
            with st.spinner("Analyzing..."):
                result = analyze_sentiment(review_text)
                
                # Display results
                st.markdown("### Sentiment Analysis Results:")
                
                # Create three columns for metrics
                col1, col2, col3 = st.columns(3)
                
                # Helper function to get sentiment emoji and color
                def get_sentiment_info(label, score):
                    if score >= 4.5:
                        return "😍", "#28a745", "Very Positive"
                    elif score >= 4.0:
                        return "😊", "#28a745", "Positive"
                    elif score >= 3.0:
                        return "😐", "#ffc107", "Neutral"
                    elif score >= 2.0:
                        return "☹️", "#dc3545", "Negative"
                    else:
                        return "😢", "#dc3545", "Very Negative"
                
                sentiment_emoji, sentiment_color, display_sentiment = get_sentiment_info(result['label'], result['score'])
                
                with col1:
                    st.markdown("**Overall Sentiment**")
                    st.markdown(f"""
                        <div style='background-color: {sentiment_color}; 
                                  padding: 20px; 
                                  border-radius: 10px; 
                                  text-align: center;'>
                            <div style='font-size: 2em; margin-bottom: 5px;'>{sentiment_emoji}</div>
                            <h2 style='color: white; margin: 0;'>{display_sentiment}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("**Rating Score**")
                    score_color = "#28a745" if result['score'] >= 4 else "#ffc107" if result['score'] >= 3 else "#dc3545"
                    st.markdown(f"""
                        <div style='background-color: {score_color}; 
                                  padding: 20px; 
                                  border-radius: 10px; 
                                  text-align: center;'>
                            <div style='font-size: 2em; margin-bottom: 5px;'>⭐</div>
                            <h2 style='color: white; margin: 0;'>{result['score']:.1f}/5</h2>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown("**Analysis Confidence**")
                    confidence_color = "#28a745" if result['confidence'] >= 80 else "#ffc107" if result['confidence'] >= 60 else "#dc3545"
                    st.markdown(f"""
                        <div style='background-color: {confidence_color}; 
                                  padding: 20px; 
                                  border-radius: 10px; 
                                  text-align: center;'>
                            <div style='font-size: 2em; margin-bottom: 5px;'>🎯</div>
                            <h2 style='color: white; margin: 0;'>{result['confidence']:.1f}%</h2>
                        </div>
                        """, unsafe_allow_html=True)

    elif st.session_state.current_page == "Assistant":
        st.title("AI Travel Assistant")
        
        # Initialize chat history in session state if not exists
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Display chat interface
        st.markdown("### Your Personal Travel Guide")
        st.markdown("Ask me anything about travel planning, safety tips, packing advice, or local recommendations!")
        
        # Display chat history
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**Assistant:** {message['content']}")
        
        # Input for new question
        user_input = st.text_input("Your question:", key="user_question")
        
        if st.button("Ask", type="primary"):
            if user_input:
                # Add user message to chat history
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                
                # Get specific response using the new function
                response = get_travel_response(user_input)
                
                # Add assistant response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                # Rerun to show new messages
                st.experimental_rerun()
        
        # Clear chat button
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.experimental_rerun()
        
        # Show example questions
        with st.expander("Example questions you can ask"):
            st.markdown("""
            - What should I pack for my trip?
            - What are some travel safety tips?
            - How should I plan my travel budget?
            - What are some cheap travel destinations?
            - How much money do I need for specific countries?
            - What transportation options should I consider?
            - How do I find good accommodation?
            - What cultural considerations should I keep in mind?
            - What's the weather like? (I'll direct you to weather services)
            """)

    else:
        st.info("Coming soon! This feature is under development.")

if __name__ == "__main__":
    main() 