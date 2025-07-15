# model/mock_predict.py
import random

def predict_waste(image):
    waste_types = ["Plastic Bottle", "Food Wrapper", "Battery", "Aluminum Can", "Paper", "E-Waste"]
    return random.choice(waste_types)
