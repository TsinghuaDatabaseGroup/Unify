import hnswlib
import time

class indexHNSW:
    def __init__(self, chunks, embeddings, chunkIDs, all_chunk_locs):
        # embeddings for the data

        self.ids = chunkIDs
        # count the number of distinct values in self.ids
        import numpy as np
        self.docNum = np.unique(self.ids).shape[0]
        self.chunks = chunks
        self.embeddings = embeddings
        self.all_chunk_locs = all_chunk_locs

        st_time = time.time()
        # todo build a hnsw index for the embeddings
        self.index = hnswlib.Index(space='cosine', dim=embeddings[0].shape[0])
        self.index.init_index(max_elements=len(embeddings), ef_construction=200, M=16)
        self.index.add_items(embeddings)
        self.index.set_ef(50)

        print("#######  Index build time: ", time.time() - st_time)


    def search(self, query, embedModel, K=int(5)):
        # Calculate embedding for the query
        query_embedding = embedModel.calculate_embeddings([query])

        # search using self.index
        st_time = time.time()
        labels, distances = self.index.knn_query(query_embedding, k=K)
        retrieval_results = self.chunks[labels]
        result_file_ids = self.ids[labels]
        print("#######  Search time: ", time.time() - st_time)

        retrieval_results = retrieval_results[0]
        result_file_ids = result_file_ids[0]

        result_chunk_locs = [self.all_chunk_locs[label_id] for label_id in labels[0]]
        return retrieval_results, result_file_ids, result_chunk_locs