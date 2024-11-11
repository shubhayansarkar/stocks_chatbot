from src.utils import rag, web_scraper
from src.logger import logger


if __name__ == "__main__":
    chain = web_scraper
    with open('graph.png', 'wb') as png:
        png.write(chain.get_graph().draw_mermaid_png())
    output = chain.invoke("Weather in Kolkata")
    # retriever = output.as_retriever()
    # print(retriever)
    print(output)