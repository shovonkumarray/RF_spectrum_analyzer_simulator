from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

def generate_spectrum(center_freq, span, rbw, amplitude):
    num_points = 1000
    freq_start = center_freq - span / 2
    freq_end = center_freq + span / 2
    frequencies = np.linspace(freq_start, freq_end, num_points)
    
    amplitudes = np.ones(num_points) * -100  # Noise floor at -100 dBm
    
    signal_freqs = [center_freq - span/4, center_freq, center_freq + span/4]
    signal_amps = [amplitude - 20, amplitude - 10, amplitude - 15]
    
    for sig_freq, sig_amp in zip(signal_freqs, signal_amps):
        sigma = rbw / 1000 / 2.355  # Convert RBW to sigma for Gaussian
        amplitudes += sig_amp * np.exp(-((frequencies - sig_freq)**2) / (2 * sigma**2))
    
    noise = np.random.normal(0, 2, num_points)
    amplitudes += noise
    
    return frequencies.tolist(), amplitudes.tolist()

@app.route('/')
def index():
    return render_template('rf_spectrum_index.html')

@app.route('/get_spectrum', methods=['POST'])
def get_spectrum():
    try:
        data = request.get_json()
        center_freq = float(data['centerFreq'])
        span = float(data['span'])
        rbw = float(data['rbw'])
        amplitude = float(data['amplitude'])
        
        frequencies, amplitudes = generate_spectrum(center_freq, span, rbw, amplitude)
        return jsonify({'frequencies': frequencies, 'amplitudes': amplitudes})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)