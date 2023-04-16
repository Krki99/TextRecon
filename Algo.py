import os
import pytesseract
from PIL import Image
import PyPDF2

# Directory containing previously collected register forms
REGISTER_FORMS_DIR = "path/to/register_forms"  # Update with your own directory path

# Load previously collected register forms
register_forms = []
for file_name in os.listdir(REGISTER_FORMS_DIR):
    file_path = os.path.join(REGISTER_FORMS_DIR, file_name)
    if file_path.endswith(".txt"):
        with open(file_path, 'r') as f:
            register_forms.append(f.read())
    elif file_path.endswith(".pdf"):
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                register_forms.append(page.extract_text())

# Define similarity threshold for determining if a text contains a register
SIMILARITY_THRESHOLD = 0.7  # Update with your desired similarity threshold

def extract_registers_from_datasheet(text):
    """
    Extracts registers from a given text if they match with previously collected register forms.

    Args:
        text (str): Input text to be analyzed.

    Returns:
        list: List of extracted register information.
    """
    extracted_registers = []
    for form in register_forms:
        extracted_register = extract_register_from_text(text, form)
        if extracted_register:
            extracted_registers.append(extracted_register)
    return extracted_registers

def extract_register_from_text(text, form):
    """
    Extracts register information from a given text if it matches with a previously collected register form.

    Args:
        text (str): Input text to be analyzed.
        form (str): Register form to compare against.

    Returns:
        str: Extracted register information if match is found, None otherwise.
    """
    similarity = similarity_score(text, form)
    if similarity > SIMILARITY_THRESHOLD:
        return text
    return None

def similarity_score(text1, text2):
    """
    Calculates similarity score between two texts using a simple cosine similarity approach.

    Args:
        text1 (str): First input text.
        text2 (str): Second input text.

    Returns:
        float: Similarity score between 0 and 1, where 0 indicates no similarity and 1 indicates identical texts.
    """
    words1 = text1.lower().split()
    words2 = text2.lower().split()
    words = list(set(words1) | set(words2))
    word_vector1 = [words1.count(word) for word in words]
    word_vector2 = [words2.count(word) for word in words]
    dot_product = sum([word_vector1[i] * word_vector2[i] for i in range(len(words))])
    norm1 = sum([word_vector1[i] ** 2 for i in range(len(words))]) ** 0.5
    norm2 = sum([word_vector2[i] ** 2 for i in range(len(words))]) ** 0.5
    similarity = dot_product / (norm1 * norm2) if (norm1 * norm2) > 0 else 0
    return similarity

# Example usage
input_text = "This is a sample datasheet text containing register information."  # Replace with your own input text
extracted_registers = extract_registers_from_datasheet(input_text)
if extracted_registers:
    print("Extracted register information:")
    for register in extracted_registers:
        print(register)
else:
    print("No register information extracted.")
