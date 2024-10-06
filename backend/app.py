from flask import Flask, jsonify, request
from star_data_processor import process_star_data, load_exoplanet_data

app = Flask(__name__)

# PLACEHOLDER: Replace 'exoplanet_data.csv' with the path to your actual CSV file
exoplanets = load_exoplanet_data('exoplanet_data.csv')

@app.route('/api/exoplanets', methods=['GET'])
def get_exoplanets():
    return jsonify(exoplanets.to_dict(orient='records'))

@app.route('/api/stars', methods=['GET'])
def get_stars():
    exoplanet_id = int(request.args.get('exoplanet'))
    exoplanet = exoplanets.iloc[exoplanet_id]
    stars = process_star_data(exoplanet['ra'], exoplanet['dec'], exoplanet['sy_dist'])
    return jsonify(stars)

if __name__ == '__main__':
    app.run(debug=True)