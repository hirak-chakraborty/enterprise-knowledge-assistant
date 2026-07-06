from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkService:

    def split(self, text: str):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            separators=[
                "\n\n",
                "\n",
                ".",
                " ",
                ""
            ]
        )

        return splitter.split_text(text)