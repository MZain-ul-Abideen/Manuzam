from features import extract_total_features

# Path to a test audio file
audio_path = "/home/zain/Desktop/Documents/Study Material/Semester 2/TER/manuzam/backend/app/Data/machine-2/audio/normal/normal_audio_2.mp3"

# Simulate machine data (like a dict returned by .dict())
machine = {
    "year_of_installation": 2019,
    "expected_lifespan": 15,
    "operating_hours_per_day": 12.0
}

# Simulate sensor data
sensor = {
    "temperature_value": 45.7,
    "vibration_value": 2.3
}

features = extract_total_features(audio_path, machine, sensor)
print("Feature vector shape:", features.shape)
print("Feature vector:", features)
