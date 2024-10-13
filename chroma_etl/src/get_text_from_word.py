from spire.doc import *


def from_word_to_txt(input_path, filenames, output_path):
    for my_file in filenames:
        my_word_file = input_path + my_file + ".docx"
        # Create a Document object
        document = Document()
        # Load a Word document
        document.LoadFromFile(my_word_file)

        # Extract the text of the document
        document_text = document.GetText()

        # Write the extracted text into a text file
        my_txt_file = output_path + my_file + ".txt"
        with open(my_txt_file, "w", encoding="utf-8") as file:
            file.write(document_text)

        # Close Document object
        document.Close()