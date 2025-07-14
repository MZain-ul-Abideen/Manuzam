# /home/zain/Desktop/Documents/Study Material/Semester 2/TER/manuzam/backend/ml/tests/inspect_model.py

from joblib import load
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend to avoid Wayland/Qt issues

import matplotlib.pyplot as plt
import numpy as np
import os

# Path to the trained model
model_path = "../saved_models/machine_5_20250701165333.joblib"

# Load the model
model = load(model_path)

# Print the model structure
print("Model structure:\n", model)

# Raw feature importance values (print before plotting)
if hasattr(model, 'feature_importances_'):
    print("\nRaw feature importances:")
    print(np.array(model.feature_importances_))
    print("\nSum of importances:", np.sum(model.feature_importances_))

# Output directory for the plot
output_plot_path = "feature_plot.png"

# Visualize feature importances (if available)
if hasattr(model, 'feature_importances_'):
    print("Visualizing feature importances...")
    plt.figure(figsize=(10, 5))
    plt.bar(np.arange(len(model.feature_importances_)), model.feature_importances_)
    plt.title("Feature Importances of Trained Model")
    plt.xlabel("Feature Index")
    plt.ylabel("Importance")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_plot_path)
    print(f"✅ Plot saved as: {output_plot_path}")

elif hasattr(model, 'coef_'):
    print("Visualizing model coefficients...")
    plt.figure(figsize=(10, 5))
    plt.bar(np.arange(len(model.coef_[0])), model.coef_[0])
    plt.title("Model Coefficients")
    plt.xlabel("Feature Index")
    plt.ylabel("Coefficient Value")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_plot_path)
    print(f"✅ Plot saved as: {output_plot_path}")

else:
    print("⚠️ This model does not expose feature importances or coefficients.")
