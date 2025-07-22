from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

def generate_spectrum(center_freq, span, rbw, amplitude):
    # Generate frequency points
    num_points = 1000
    freq_start = center_freq - span / 2
    freq_end = center_freq + span / 2
    frequencies = np.linspace(freq_start, freq_end, num_points)
    
    # Simulate spectrum with some signals
    amplitudes = np.ones(num_points) * -100  # Noise floor at -100 dBm
    
    # Add some simulated signals
    signal_freqs = [center_freq - span/4, center_freq, center_freq + span/4]
    signal_amps = [amplitude - 20, amplitude - 10, amplitude - 15]
    
    for sig_freq, sig_amp in zip(signal_freqs, signal_amps):
        # Gaussian-shaped signal
        sigma = rbw / 1000 / 2.355  # Convert RBW to sigma for Gaussian
        amplitudes += sig_amp * np.exp(-((frequencies - sig_freq)**2) / (2 * sigma**2))
    
    # Add some random noise
    noise = np.random.normal(0, 2, num_points)
    amplitudes += noise
    
    return frequencies.tolist(), amplitudes.tolist()

@app.route('/get_spectrum', methods=['POST'])
def get_spectrum():
    data = request.get_json()
    center_freq = data['centerFreq']
    span = data['span']
    rbw = data['rbw']
    amplitude = data['amplitude']
    
    frequencies, amplitudes = generate_spectrum(center_freq, span, rbw, amplitude)
    return jsonify({'frequencies': frequencies, 'amplitudes': amplitudes})

if __name__ == '__main__':
    app.run(debug=True)