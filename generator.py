from llm import llm
from few_shots import FewShotPosts

few_shot = FewShotPosts()

def get_prompt(length, language, tag):
    length_str = get_len(length)
    prompt = f'''
        Generate a LinkedIn post using the below information. No preamble.

        1) Topic: {tag}
        2) Length: {length_str}
        3) Language: {language}
        If Language is Hinglish then it means it is a mix of Hindi and English. 
        The script for the generated post should always be English.
        
        Output Constraints:
        - The post must be {length_str} long.
        - Each sentence should be concise.
        - Do NOT exceed the specified line limit.
        - Maintain proper LinkedIn-style formatting.

        '''
    examples = few_shot.get_filtered(length, language, tag)
    if len(examples) > 0:
        prompt += "4) use these examples to capture the writing style"
        for i, post in enumerate(examples):  # in order to also get the index of the post
            post_text = post['text']
            prompt += f'\n\n Example {i + 1}: \n\n {post_text}'
            if i == 1:  # max two samples
                break
    return prompt


def generate(length, language, tag): # this is the function that deals with the post generation
    prompt = get_prompt(length,language,tag)
    response = llm.invoke(prompt)
    return response.content


def get_len(length):
    if length == "SHORT":
        return "1 to 5 lines"
    if length == "MEDIUM":
        return "6 to 10 lines"
    if length == "LONG":
        return "11 to 15 lines"

if __name__ == "__main__":
    post = generate("SHORT","English", "Scam")
    print(post)
