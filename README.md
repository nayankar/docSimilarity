# docSimilarity
Document Similarity using Shingling, Min-Hashing &amp; LSH

- In this assignment you will explore the use of Shingling, Jaccard Similarity, Min Hashing, and LSH in the context of document
similarity.

## Input parameters to run the code :
- folder_path_containing_docs: The path to the folder containing the text files.
- k: Value of k used while making k-shingles.
- type_of_shingles: The type of shingles you have to consider. The two possible values are char/word.
- If the input parameter is set as char, you have to construct k-shingles based on characters.
- If the input parameter is set as word, you have to construct k-shingles based on words.
- no_of_hashes_for_minhashing: No of hash functions to be used for Min-hashing.
- threshold_value: The threshold value s used in LSH which defines how similar the documents have to be for them to be
considered as similar pair.
