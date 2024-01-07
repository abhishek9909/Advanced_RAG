from completion import stream_completion
import asyncio
from ingestion import prepare_text


async def print_completion():
    async for x in stream_completion("Write a poem on America in 50 words or less"):
        print(x)

if __name__ == "__main__":
    #asyncio.run(print_completion())
    #print(prepare_text("../assets/mock_input/Professional_Resume.pdf", extension='.pdf'))
    print(prepare_text("../assets/mock_input/sample_pdf.pdf", extension='.pdf', data_type='image'))