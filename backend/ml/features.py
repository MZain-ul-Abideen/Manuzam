import librosa
import numpy as np
import datetime


def extract_audio_features(file_path: str, sr: int = 22050):
    y, sr = librosa.load(file_path, sr=sr)
    
    # Extract MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfccs_mean = np.mean(mfccs, axis=1)

    # Zero Crossing Rate
    zcr = np.mean(librosa.feature.zero_crossing_rate(y))

    # Spectral Centroid
    spec_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))

    return list(mfccs_mean) + [zcr, spec_centroid]


def extract_machine_features(machine: dict):
    # machine is a dictionary from DB (SQLAlchemy or pydantic model.dict())
    current_year = datetime.datetime.now().year
    install_year = machine.get("year_of_installation", current_year)
    lifespan = machine.get("expected_lifespan", 0)
    op_hours = machine.get("operating_hours_per_day", 0.0)

    return [
        current_year - install_year,  # age
        lifespan,
        op_hours
    ]


def extract_sensor_features(sensor: dict):
    temp = sensor.get("temperature_value", 0.0)
    vib = sensor.get("vibration_value", 0.0)

    return [temp, vib]


def extract_total_features(audio_path: str, machine: dict, sensor: dict):
    audio_feats = extract_audio_features(audio_path)
    machine_feats = extract_machine_features(machine)
    sensor_feats = extract_sensor_features(sensor)

    return np.array(audio_feats + machine_feats + sensor_feats)
