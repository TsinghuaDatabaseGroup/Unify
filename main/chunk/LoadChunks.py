import os
from collections import defaultdict
from typing import Any, Dict, List, Tuple

import numpy as np
import ray
import torch
import vllm
from blingfire import text_to_sentences_and_offsets
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import time
import pymupdf

MAX_CONTEXT_SENTENCE_LENGTH = 1000

def load_process_data_chunks(embedModel, chunkExtractor, doc_path):
    all_chunks = []
    all_ids = []
    all_embeds = []
    all_chunk_locs = []

    # load all files in the doc_path directory to get all chunks
    all_file_data = {}  # dict of  `file_name`  and  `its data`
    for file in os.listdir(doc_path):
        print("Processing file: ", file)
        if file.endswith(".pdf"):
            doc = pymupdf.open(os.path.join(doc_path, file))
            all_data = chr(12).join([page.get_text("text") for page in doc])

        elif file.endswith(".txt"):
            # load contents in file
            with open(os.path.join(doc_path, file), "r") as f:
                all_data = f.read()
        else:
            print("Not supported yet, skip!")
            pass
        all_file_data[file] = all_data
        chunks, chunk_starts, chunk_ends = chunkExtractor.chunk_single_doc(all_data)

        chunks = np.array(chunks)
        chunk_starts = np.array(chunk_starts)
        chunk_ends = np.array(chunk_ends)
        chunk_lens = chunk_ends - chunk_starts

        embeddings = embedModel.calculate_embeddings(chunks)

        all_chunks.extend(chunks)
        all_ids.extend([file] * len(chunks))
        all_embeds.extend(embeddings)

        for start, end, LEN in zip(chunk_starts, chunk_ends, chunk_lens):
            all_chunk_locs.append((file, int(start), int(LEN)))

    all_chunks = np.array(all_chunks)
    all_ids = np.array(all_ids)
    all_embeds = np.array(all_embeds)

    return all_file_data, all_chunks, all_ids, all_embeds, all_chunk_locs