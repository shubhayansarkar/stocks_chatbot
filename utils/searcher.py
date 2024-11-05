from duckduckgo_search import DDGS

class ddg_search:
    def serach(self, query, num_web):
        r_list = []
        self.results = DDGS().text(query, max_results= num_web)
        r_list = [i['href'] for i in self.results]
        return r_list

# r = ddg_search()
# print(r.serach(query = "tata shares", num_web = 1))

