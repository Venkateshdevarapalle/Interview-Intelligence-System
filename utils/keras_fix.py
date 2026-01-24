import sys
import tf_keras

# HARD override for DeepFace compatibility
sys.modules["keras"] = tf_keras
sys.modules["tensorflow.keras"] = tf_keras
sys.modules["tensorflow.keras.models"] = tf_keras.models
sys.modules["tensorflow.keras.layers"] = tf_keras.layers
sys.modules["tensorflow.keras.backend"] = tf_keras.backend
