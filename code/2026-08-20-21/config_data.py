md5_path = "./md5.text"

# Chroma
collection_name = "rag"
persist_directory = "./chromadb"

# splitter
chunk_size = 1000
chunk_overlap = 100
separators = ['\n','\n\n','.','!','?','。','！','？']
max_split_char_nums = 1000