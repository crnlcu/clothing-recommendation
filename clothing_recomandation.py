from flask import Flask, request, render_template
from datetime import datetime, timedelta

app = Flask(__name__)

# Your baby clothing recommendation function
def baby_clothing_recommendation(dob):
    dob = datetime.strptime(dob, '%Y-%m-%d')
    growth_periods = [(0, 3), (3, 6), (6, 9), (9, 12), (12, 18), (18, 24)]
    seasons = {
        'Spring': ['03', '04', '05'],
        'Summer': ['06', '07', '08'],
        'Fall': ['09', '10', '11'],
        'Winter': ['12', '01', '02']
    }
    season_clothing = {
        'Spring': ['🧥 Light jacket', '👕 Long-sleeved shirts', '👖 Lightweight cotton pants', 
                   '🧣 Lightweight sweater', '👚 Layering t-shirts', '👒 Sun hat', 
                   '🧦 Light socks', '🧤 Light mittens', '🧸 Light blanket (for outings)'],
        'Summer': ['👕 Short-sleeved shirts', '👶 Onesies', '🩳 Shorts', '🍼 Rompers', 
                   '👗 Lightweight cotton dress', '🌞 Lightweight pajamas', '🧢 Sun hat', 
                   '🩱 Swimwear', '👡 Sandals', '🕶️ Sunglasses', '🌬️ Lightweight blanket', 
                   '🦟 Mosquito netting', '👶 Diaper covers'],
        'Fall': ['🧥 Warm jacket', '👕 Long-sleeved shirts', '👖 Fleece-lined pants', 
                 '🧶 Sweater or cardigan', '👶 Footed pajamas', '👚 Layering onesies', 
                 '🧢 Warm hat', '🧦 Warmer socks', '👢 Booties', '🧣 Light scarf', 
                 '🧸 Fleece blanket', '🧤 Mittens'],
        'Winter': ['🧥 Winter coat', '👶 Snowsuit', '👖 Warm pants', '🧶 Wool sweaters', 
                   '🧣 Thermal onesies', '👕 Layered long-sleeved shirts', '🧸 Fleece-lined pajamas', 
                   '🧢 Winter hat', '🧤 Gloves or mittens', '👢 Insulated booties', '🧦 Wool socks', 
                   '🧸 Heavy blanket', '🦻 Ear muffs', '🧣 Scarf', '🛏️ Sleeping sack']
    }
    recommendations = {}
    for period in growth_periods:
        start_month = dob.month
        end_date = dob + timedelta(days=(period[1] * 30))
        size = f'{period[0]}-{period[1]} months'
        for season, months in seasons.items():
            if str(start_month).zfill(2) in months:
                recommendations[size] = season_clothing[season]
                break
        dob = end_date
    return recommendations

@app.route('/')
def home():
    return '''
    <h1>Baby Clothing Recommendation</h1>
    <form action="/recommend" method="POST">
        Date of Birth (YYYY-MM-DD): <input type="text" name="dob">
        <input type="submit" value="Get Recommendations">
    </form>
    '''

@app.route('/recommend', methods=['POST'])
def recommend():
    dob = request.form['dob']
    recommendations = baby_clothing_recommendation(dob)
    result = "<h2>Clothing Recommendations:</h2>"
    for size, items in recommendations.items():
        result += f"<h3>{size} months:</h3><ul>"
        for item in items:
            result += f"<li>{item}</li>"
        result += "</ul>"
    return result

if __name__ == "__main__":
    app.run(debug=True)

