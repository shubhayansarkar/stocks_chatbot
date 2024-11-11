from src.utils import chain
from src.logger import logger


if __name__ == "__main__":
    with open('graph.png', 'wb') as png:
        png.write(chain.get_graph().draw_mermaid_png())
    output = chain.invoke('weather in Kolkata')
    logger.debug(f"Document Chunks: {len(output)}")