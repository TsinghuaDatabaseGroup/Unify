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


MAX_CONTEXT_SENTENCE_LENGTH = 1000

class ChunkExtractor:

    @ray.remote
    def _extract_chunks(self, interaction_id, text):
        """
        Extracts and returns chunks from given HTML source.

        Note: This function is for demonstration purposes only.
        We are treating an independent sentence as a chunk here,
        but you could choose to chunk your text more cleverly than this.

        Parameters:
            interaction_id (str): [Nonsense]  Interaction ID that this HTML source belongs to.
            text (str): content from which to extract chunks.

        Returns:
            Tuple[str, List[str]]: A tuple containing the interaction ID and a list of sentences extracted from the HTML content.
        """



        # Extract offsets of sentences from the text
        _, offsets = text_to_sentences_and_offsets(text)

        # Initialize a list to store sentences
        chunks = []
        starts = []
        ends = []

        # Iterate through the list of offsets and extract sentences
        for start, end in offsets:
            # Extract the sentence and limit its length
            sentence = text[start:end][:MAX_CONTEXT_SENTENCE_LENGTH]
            chunks.append(sentence)
            starts.append(start)
            ends.append(end)


        return interaction_id, chunks, starts, ends
    
    
    def chunk_single_doc(self, text):
        """
        Extracts and returns chunks from one doc.
        :param text (str):  The doc to be chunked
        :return: List[str]: A list of sentences extracted from the doc.
        """
        _, offsets = text_to_sentences_and_offsets(text)

        # Initialize a list to store sentences
        chunks = []
        starts = []
        ends = []

        # Iterate through the list of offsets and extract sentences
        for start, end in offsets:
            # Extract the sentence and limit its length
            sentence = text[start:end][:MAX_CONTEXT_SENTENCE_LENGTH]
            chunks.append(sentence)
            starts.append(start)
            ends.append(end)

        return chunks, starts, ends

    
    def extract_chunks(self, batch_interaction_ids, batch_search_results):
        """
        Extracts chunks from given batch search results using parallel processing with Ray.

        Parameters:
            batch_interaction_ids (List[str]): List of interaction IDs.
            batch_search_results (List[List[Dict]]): List of search results batches, each containing HTML text.

        Returns:
            Tuple[np.ndarray, np.ndarray]: A tuple containing an array of chunks and an array of corresponding interaction IDs.
        """
        # Setup parallel chunk extraction using ray remote
        ray_response_refs = [
            self._extract_chunks.remote(
                self,
                interaction_id=batch_interaction_ids[idx],
                html_source=text
            )
            for idx, search_results in enumerate(batch_search_results)
            for text in search_results
        ]

        # Wait until all sentence extractions are complete
        # and collect chunks for every interaction_id separately
        chunk_dictionary = defaultdict(list)

        for response_ref in ray_response_refs:
            interaction_id, _chunks = ray.get(response_ref)  # Blocking call until parallel execution is complete
            chunk_dictionary[interaction_id].extend(_chunks)

        # Flatten chunks and keep a map of corresponding interaction_ids
        chunks, chunk_interaction_ids = self._flatten_chunks(chunk_dictionary)

        return chunks, chunk_interaction_ids

    def _flatten_chunks(self, chunk_dictionary):
        """
        Flattens the chunk dictionary into separate lists for chunks and their corresponding interaction IDs.

        Parameters:
            chunk_dictionary (defaultdict): Dictionary with interaction IDs as keys and lists of chunks as values.

        Returns:
            Tuple[np.ndarray, np.ndarray]: A tuple containing an array of chunks and an array of corresponding interaction IDs.
        """
        chunks = []
        chunk_interaction_ids = []

        for interaction_id, _chunks in chunk_dictionary.items():
            # De-duplicate chunks within the scope of an interaction ID
            unique_chunks = list(set(_chunks))
            chunks.extend(unique_chunks)
            chunk_interaction_ids.extend([interaction_id] * len(unique_chunks))

        # Convert to numpy arrays for convenient slicing/masking operations later
        chunks = np.array(chunks)
        chunk_interaction_ids = np.array(chunk_interaction_ids)

        return chunks, chunk_interaction_ids

