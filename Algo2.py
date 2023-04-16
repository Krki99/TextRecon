import textract
from PIL import Image, ImageDraw, ImageFont
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
import joblib
import os

# Function to train a register recognition model
def train_register_recognition_model(training_data):
    # Create a CountVectorizer to convert text to numerical features
    vectorizer = CountVectorizer()
    features = vectorizer.fit_transform(training_data['text'])

    # Create a Support Vector Machine (SVM) classifier
    classifier = SVC(kernel='linear', C=1.0, random_state=42)

    # Train the model
    classifier.fit(features, training_data['label'])

    # Save the trained model
    joblib.dump(classifier, 'register_recognition_model.pkl')

    # Save the CountVectorizer for future use
    joblib.dump(vectorizer, 'count_vectorizer.pkl')

    print("Register recognition model trained and saved.")

# Function to perform text recognition on a PDF file and save registers as JPEG images
def recognize_registers(file_path):
    # Load the file using Textract
    text = textract.process(file_path, method='tesseract', language='eng')
    text = text.decode('utf-8')

    # Split text into lines
    lines = text.split('\n')

    # Load the trained model and CountVectorizer
    classifier = joblib.load('register_recognition_model.pkl')
    vectorizer = joblib.load('count_vectorizer.pkl')

    # Create a directory to save the register images
    if not os.path.exists('registers'):
        os.makedirs('registers')

    # Create an image to draw the registers on
    img = Image.new('RGB', (800, 600), color='white')
    d = ImageDraw.Draw(img)

    # Set the font for the registers
    font = ImageFont.truetype('arial.ttf', size=14)

    # Iterate through the lines of text
    for line in lines:
        # Check if the line contains a register (e.g., starts with 'R' or 'r')
        if classifier.predict(vectorizer.transform([line]))[0] == 1:
            # Draw the register on the image
            d.text((10, 10), line, fill='black', font=font)
            # Save the register as a JPEG image
            img.save(f'registers/{line}.jpeg')
            # Reset the image for the next register
            img = Image.new('RGB', (800, 600), color='white')
            d = ImageDraw.Draw(img)

    print("Registers recognized and saved as JPEG images in the 'registers' directory.")

# Example usage: train the register recognition model
training_data = {'text': ['R1', 'R2', 'R3'], 'label': [1, 1, 1]}  # Example training data
train_register_recognition_model(training_data)

# Example usage: recognize registers in a PDF file and save them as JPEG images
file_path = 'datasheet.pdf'
recognize_registers(file_path)
