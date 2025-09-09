import requests

WORD_API: str = "https://random-word-api.herokuapp.com/word?"


def retrieve_word(length: int = 10) -> str:
    if length > 14 or length <= 3:
        raise ValueError("length parameter must be below 14 and greater than 3")
    while True:
        query_api: str = f"{WORD_API}length={length}"
        response: requests.Response = requests.get(query_api)
        if not response.ok:
            continue
        words: list[str] = response.json()
        return words[0]
    

if __name__ == "__main__":
    print(retrieve_word(10))