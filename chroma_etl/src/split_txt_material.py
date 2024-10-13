from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_as_documents(filename_list, input_path, chunk_size, chunk_overlap):

    my_splitter = RecursiveCharacterTextSplitter(
        # Specify max. chunk size and overlap
        # What size can I have for my embedder?
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )

    all_text_chunks = []
    for my_file in filename_list:
        my_txt_file = input_path + my_file + ".txt"
        with open(my_txt_file, encoding="utf8") as f:
            my_txt_file_content = f.read()

        # Create chunks as LangChain Documents for further processing in LangChain
        langchain_doc_chunks = my_splitter.create_documents([my_txt_file_content])
        print(my_file + " has " + str(len(langchain_doc_chunks)) + " chunks.")

        # add year as metadata
        year_published = my_file[-4:]
        for idx, chunk in enumerate(langchain_doc_chunks):
            langchain_doc_chunks[idx].metadata["published_year"] = year_published
        for chunk in langchain_doc_chunks:
            all_text_chunks.append(chunk)
    print("The total number of text chunks from all documents is: " + str(len(all_text_chunks)))
    # print(all_text_chunks[1])
    return all_text_chunks


def chunk_as_strings(filename_list, input_path, output_path, chunk_size, chunk_overlap):

    # Create text splitter
    my_splitter = RecursiveCharacterTextSplitter(
        # Specify max. chunk size and overlap
        # What size can I have for my embedder?
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )

    # Read files to be split
    for my_file in filename_list:
        my_txt_file = input_path + my_file + ".txt"
        with open(my_txt_file, encoding="utf8") as f:
            my_txt_file_content = f.read()

        # Create chunks as strings
        string_split = my_splitter.split_text(my_txt_file_content)

        # The splitter function tries to keep text from one paragraph together.
        # If that is not possible, then keep sentences together. However, sentences are identified as
        # terminated by "\n", which is not the case for my text. Should/Can I change that?
        # If I add "." to the splitter character list, then it will split after abbreviation points.
        # The overlap ensures, text is repeated, so the chances are higher that it is in the correct chunk.
        # Seems like there is no repetition when the chunk ends with the end of a sentence or paragraph.
        # Alternatively, I can use another splitter function from NLP library that splits by sentence.
        # But do I want 1 sentence in a chunk or rather several sentences up to 1 paragraph?

        # Save chunked file as txt (for human review)
        splitted_file = output_path + my_file + "_chunked.txt"
        number_of_chunk = 1

        with open(splitted_file, 'w', encoding="utf8") as f:
            for text in string_split:
                f.write("Chunk Nr." + str(number_of_chunk) + '\n')
                f.write(text + '\n\n')
                number_of_chunk += 1
            print(splitted_file + " has " + str(number_of_chunk) + " chunks.")


