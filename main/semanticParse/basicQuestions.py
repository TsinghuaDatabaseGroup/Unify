from .logicalRepresentations import *
import re

# Store all logical representations
BasicQuestions = [
    FILTER_LR,
    FILTER_LR_2,
    COUNT_LR_2,
    COUNT_LR_3,
    CONDITIONAL_LR,
    CONDITIONAL_LR_2,
    CONDITIONAL_LR_3,
    CONDITIONAL_LR_4,
    COMPARE_LR,
    COMPARE_LR_2,
    COMPARE_MULTIPLE_LR,
    GROUPBY_LR,
    COMPUTE_RATIO_LR,
    CONDITIONAL_LR,
    CONDITIONAL_LR_2,
    COMPLEMENTARY_LR,
    EXTRACT_LR,
    INTERSECTION_LR,
    JOIN_LR,
    SUM_LR
]


class BQMatcher():
    def __init__(self, embedModel):
        self.basicQuestions = BasicQuestions
        self.embedModel = embedModel
        self.BQEmbeddings = self.embedQuestions()

    def embedQuestions(self):
        return [self.embedModel.calculate_embeddings(q["Question"]) for q in self.basicQuestions]

    def match(self, query,  topK=1):
        """
            :param query: str, the query to be matched (parsed form)
            :param topK: int, the number of matches
            :return: list, the matched basic questions (length is topK)
        """        
        # If template matching fails, perform embedding similarity matching    
        queryEmbed = self.embedModel.calculate_embeddings(query)
        cosine_scores = (self.BQEmbeddings * queryEmbed).sum(1)

        # return topK best matches, higher score should be better
        bestMatches = cosine_scores.argsort()[-topK:][::-1]

        print(f"==== matchedBQ   top [{topK}] ====")
        for i in range(topK):
            # set 5 float points for the first output
            print(f"  {cosine_scores[bestMatches[i]]:.5f}", self.basicQuestions[bestMatches[i]]["IDQuestion"])
        print()
        return [self.basicQuestions[i] for i in bestMatches]

