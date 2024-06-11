import requests
import json

corpus_of_documents = [
    "Sentences that express that something is important, but not what, are 'tvw' errors",
    "A phrase that indicates tvw is 'is important' and its variants",
    "A phrase that indicates tvw is 'is crucical' and its variants",
    "An example of tvw is the sentence 'listening to others is important'",
]

def jaccard_similarity(query, document):
  query = query.lower().split(" ")
  document = document.lower().split(" ")
  intersection = set(query).intersection(set(document))
  union = set(query).union(set(document))
  return len(intersection)/len(union)

def return_response(query, corpus):
    similarities = []
    for doc in corpus:
        similarity = jaccard_similarity(query, doc)
        similarities.append(similarity)
    return corpus_of_documents[similarities.index(max(similarities))]

user_input = """Identify sentences with 'that versus what' errors in this essay We’ve all scrolled through Tik Tok, read the news, even read opinion articles in the New York Times. We learn from what other people say and think through these mediums. But at what point can we discern our own thoughts and opinions from the amalgamation of what we see online? How do we maintain our own opinions when we’re so constantly bombarded with others’? We should look to maintain our own autonomy and opinions for both personal growth and to avoid singular narratives; however, we also have to be receptive to others’ thoughts (not necessarily assimilate to them) to inform our own.
        We need to maintain autonomy over our own thoughts and opinions because it helps us grow personally and avoid becoming a homogenous whole, or only adhering to a singular narrative. This is easier said than done, though. It’s also much easier to think for ourselves in solitude, when we’re not constantly bombarded by others’ opinions. Thoreau wrote some of his best work when secluded alone in the wilderness, using his solitude as a medium for personal reflection and a way to interpret the world around him. Evidently, we have a lot to gain from simply being with our own thoughts. It’s important to understand what our own opinions are, not only to understand ourselves, but also how we perceive others or what lens we observe the world with. In this manner, we understand our own biases and can understand how to improve. We’re also generally more creative when we’re left with our own thoughts rather than being informed by others, which can lead us to succeed through producing art and other works. Nonetheless, Thoreau’s work and introspection was spent in solitude — it’s much harder to maintain our own thoughts when we’re being bombarded with so many other narratives and opinions, but we must do it to maintain a diverse society. Notably, Thurber was a humorist who wrote diatribes against the United States government when there was a great fear of communism and ideas concerning censorship were beginning to circulate. We’ve all been in environments (say, a test…) when the emotion is palpable. It’s so easy to feel all of the nervousness or fear accumulating in a room, or city, or country, and to go along with it. When others voice their fears and opinions, we too easily let them become our own. The issue with this is that the general opinion isn’t always right. When we fail to maintain our own thoughts and ideas, it lets us simply become some homogenous whole, which easily becomes prejudiced, emotional, or dangerous. It certainly is harder to maintain our own opinions when surrounded with others, but we must do so to keep a diverse society.
        Nonetheless, we can’t be too close minded; we have to be receptive to others’ ideas and even while maintaining our own because we always can learn and collaboration produces great work. When the US pulled out of the Paris climate agreement (despite the outcry from scientists, statisticians, and the like), we saw a time in which it was important to listen to others. Our personal knowledge is limited and flawed. We have our own areas of expertise, and others have their own. When people have a veritable, facts-based opinion, then we should listen and learn from it. In this manner, we become more informed people. This doesn’t necessarily mean that we need to adhere to their direct line of thought. Rather, we should use others’ expertise and opinions to inform our own, not maintain solitude to the point where we close ourselves off. We also can benefit from working with others. During the Enlightenment, philosophes would gather in salons, or scientists would gather at universities and academies (say Cambridge, University of Paris, etc…) to learn from one another, producing fundamental theories and works that inform our governments, societies, and rights today. This spirit of collaboration has continued into the modern day, say even the global support that the Iranian soccer team has received in light of threats and violence from their own government. We not only can learn from others, but we can benefit from collaboration. It’s a bit of a cliché, but more brains are better than just one. It’s important that we don’t blindly adhere to beliefs, or too easily discard our own, but some of the best work humans have done emerges from when we all work together. This allows us to meld the best parts of everyone’s thinking and create a product which can benefit the whole. There have been times when singular scientists, or thinkers, have worked best in solitude, say Paul Erdos (a great mathematician), who would take strolls on his own and simply work in his head, or (as previously mentioned), Thoreau. We can come up with amazing, creative ideas on our own. We all have personal merit and knowledge which can suffice without the others. Nonetheless, it can be easier to work with others, or build off of their thoughts. Through collaboration, where we allow ourselves to learn and simultaneously maintain independence, we tend to learn, grow, and create amazing things as a whole.
        Even as we read, watch videos, or hear the opinions of others, our own perceptions and thoughts are being influenced by others’. It can be inherently damaging to not maintain some sense of individuality or solitude in thought, melding us with the whole, or causing us to lose ourselves. Nonetheless, solitude is also deeply flawed, leading to narrow and uninformed conceptions. We ultimately have to strike some sort of a balance, based on our own level of experience and knowledge. As a student, I know I have to be receptive, to grow and to learn — I haven’t seen enough of the world to staunchly stick to my own opinions. I have to collaborate and learn from others. Another might not have to be as receptive as me, with more experience in the world and informed opinions. We all have our own personal balance to find, both between solitude and collaboration."""
relevant_document = return_response(user_input, corpus_of_documents)
full_response = []

prompt = f"""
You are a bot that identifies 'that versus what' errors in essays. You answer in very short sentences and do not include extra information.
This is a common error in essays: {relevant_document}
The user input is: {user_input}
Compile a recommendation to the user based on the recommended activity and the user input.
"""

url = 'http://localhost:11434/api/generate'

data = {
    "model": "llama2",
    "prompt": prompt.format(user_input=user_input, relevant_document=relevant_document)
}
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data=json.dumps(data), headers=headers, stream=True)
try:
    count = 0
    for line in response.iter_lines():
        if line:
            decoded_line = json.loads(line.decode('utf-8'))
            
            full_response.append(decoded_line['response'])
finally:
    response.close()

print(''.join(full_response))