class indexPlain:
    def __init__(self, chunks, embeddings, chunkIDs):
        # embeddings for the data

        self.ids = chunkIDs
        self.chunks = chunks
        self.embeddings = embeddings


    def search(self, query, embedModel, K=int(5)):
        # Calculate embeddings for the query
        query_embedding = embedModel.calculate_embeddings([query])

        # todo: set relevant_chunks_embeddings correctly
        # Calculate cosine similarity between query and chunk embeddings,
        cosine_scores = (self.embeddings * query_embedding).sum(1)


        topK_idx = (-cosine_scores).argsort()[:K]
        # and retrieve top-N results.
        retrieval_results = self.chunks[
            topK_idx
        ]
        result_file_ids = self.ids[
            topK_idx
        ]

        return retrieval_results, result_file_ids