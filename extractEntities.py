import textrazor
import os
import codecs


textrazor.api_key = "ad28e70f9a5a3b3bb845be859788525bed6b6870d6b20a4d14f0afbd"


# config
client = textrazor.TextRazor(extractors=["entities", "topics","entailments","relations"])
#client = textrazor.TextRazor(extractors=["entities"])
client.set_cleanup_mode("cleanHTML")


url = "http://www.gpgroot.nl"

response = client.analyze_url(url)
entailments = list(response.entailments())
relations = list(response.relations())
topics = list(response.topics())
entities = list(response.entities())

entities.sort(key=lambda x: x.relevance_score, reverse=True)

seen = set()
print topics
for topic in topics:
    if topic.id not in seen:
        print topic.id, topic.label, topic.score
        seen.add(topic.id)

for relation in relations:
    print relation.predicate_words, relation.params, relation.predicate_positions




#for entity in entities:
#    if entity.id not in seen:
#        print entity.id, entity.relevance_score, entity.confidence_score, entity.freebase_types
#        seen.add(entity.id)








