import bz2
import json
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

from transformers import LlamaTokenizerFast
from sentence_transformers import SentenceTransformer
import torch

SENTENTENCE_TRANSFORMER_BATCH_SIZE = 128 # TUNE THIS VARIABLE depending on the size of your embedding model and GPU mem available


class EmbedModel:
    def __init__(self, tokenizer_path, sentence_model_path):
        # Load tokenizer
        self.tokenizer = LlamaTokenizerFast.from_pretrained(tokenizer_path)
        self.sentence_model = SentenceTransformer(
            # "models/sentence-transformers/all-MiniLM-L6-v2",
            sentence_model_path,
            device=torch.device(
                "cuda" if torch.cuda.is_available() else "cpu"
            ),
        )


    def calculate_embeddings(self, sentences):
        """
        Compute normalized embeddings for a list of sentences using a sentence encoding model.

        This function leverages multiprocessing to encode the sentences, which can enhance the
        processing speed on multi-core machines.

        Args:
            sentences (List[str]): A list of sentences for which embeddings are to be computed.

        Returns:
            np.ndarray: An array of normalized embeddings for the given sentences.

        """
        embeddings = self.sentence_model.encode(
            sentences=sentences,
            normalize_embeddings=True,
            batch_size=SENTENTENCE_TRANSFORMER_BATCH_SIZE,
        )
        return embeddings