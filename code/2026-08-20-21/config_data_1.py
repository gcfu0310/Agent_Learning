md5_path = "./md5_1.text"

# Chroma
collection_name = "rag_1"
persist_directory = "./chromadb_1"

# splitter
chunk_size = 150#1000
chunk_overlap = 0#100
separators = ['\n','\n\n','.','!','?','。','！','？']
max_split_char_nums = 1000