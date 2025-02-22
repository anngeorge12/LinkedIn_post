from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm import llm
import json

# reading the json file that has been loaded


def process_posts(raw_file_path, processed_file_path="data/processed_posts.json"):
    enrich_post=[]
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        for post in posts:
            try:
                metadata = extract_metadata(post["text"])  # Extract metadata
                post_metadata = post | metadata  # Merge original post & extracted metadata
                enrich_post.append(post_metadata)
            except UnicodeEncodeError as e:
                print(f"Unicode error in post: {post['text'][:100]}... Skipping problematic characters.")
                continue

    unified_tags = get_unified_tags(enrich_post)
    for post in enrich_post:
        current = post['tags'] # to get the tags that are genrated currently
        new_tags = {unified_tags[tags] for tags in current}  # used for comprehending set all common tags have one name
        post['tags'] = list(new_tags)

    with open(processed_file_path,encoding='utf-8', mode='w') as outfile:
        json.dump(enrich_post,outfile,indent=4) # for writing into a new json file all the tags obtained


def get_unified_tags(posts_metadata):  # used for getting common tags as a single tag name for easier working
    unique_tags = set() # set is used to make sure to remove the duplicates
    for p in posts_metadata:
        unique_tags.update(p['tags'])

    unique_tags_list = ','.join(unique_tags)

    template = '''I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list. 
       Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search". 
       Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
       Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
       Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
    2. Each tag should be follow title case convention. example: "Motivation", "Job Search"
    3. Output should be a JSON object, No preamble
    3. Output should have mapping of original tag and the unified tag. 
       For example: {{"Jobseekers": "Job Search",  "Job Hunting": "Job Search", "Motivation": "Motivation}}
    
    Here is the list of tags: 
    {tags}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": str(unique_tags_list)})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return res


# this func gives the details like language, line count and heading etc


def extract_metadata(post):
    template = '''
    You are given a LinkedIn Post,You have to extract the number of lines, language used and the tags in the post.
    1.Return a valid JSON.No preamble
    2.JSON object should have exactly these 3 keys: line_count,language and tags.
    3. tags should be in an array of text tags.Extract a minimum of two or three tags.
    4. Language should be  English or Hinglish( a mix of hindi+english)
    
    
    Here is the post on which you perform the task:
    {post}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    try:
        response = chain.invoke({'post': post})

        if not response or not hasattr(response, "content"):
            raise ValueError("Invalid response from LLM")

        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
        return res

    except (OutputParserException, ValueError) as e:
        print(f"Error processing post: {post[:100]}...\nError: {e}")
        return {"line_count": 0, "language": "Unknown", "tags": []}  # Return default JSON

# this llm will help in calling our llama model
    # the bar operator will help in creating a chain that helps in supplying it as a continous promt to our llama
# we will use prompt template from langchain to replace the actual post in the given sentence
# we say no preamble to avoid the first set of text that the model gives like an answer


if __name__ == "__main__":
    process_posts("data/raw_post.json", "data/process_posts.json")