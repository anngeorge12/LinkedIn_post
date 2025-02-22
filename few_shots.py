import pandas as pd
import json
class FewShotPosts:
    def __init__(self, filepath="data/process_posts.json"):
        self.df = None
        self.unique_tags = None
        self.load_posts(filepath)

    def load_posts(self, file_path): #the prupose of this function is to populate this file path
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)
            df = pd.json_normalize(posts) # converting the json dict into a pandas dataframe
            df["length"] = df["line_count"].apply(self.categorise_length) # create a new column in the data frame to label short med or long
            all_tags = df["tags"].apply(lambda x: x).sum()
            self.unique_tags = set(list(all_tags)) # this function is to obtain all the unique tags
            self.df = df

    def categorise_length(self, line_count): # this func is to return the range of line count as short,med,lng
        if line_count<5:
            return 'SHORT'
        elif line_count>=5 and line_count<=10:
            return 'MEDIUM'
        else:
            return 'LONG'

    def get_tags(self):
        return self.unique_tags


    def get_filtered(self,length,language, tag): # this function is to get specifically selected posts
        df_filtered = self.df[
            (self.df['language'] == language) & (self.df['length'] == length) &
            (self.df['tags'].apply(lambda tags: tag in tags)) #if you have a list checking if the unique tag is present in the list
        ]
        return df_filtered.to_dict(orient="records")

if __name__ == "__main__" :
    fs = FewShotPosts()
    posts = fs.get_filtered("SHORT", "Hinglish", "Job Search")
    print(posts)


