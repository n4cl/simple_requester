import sys
from concurrent import futures

import requests

class SimpleRequester:
    def __init__(self, url: str, concurrent: int = 0) -> None:
        self.url = url
        self.concurrent = concurrent

    def request(self):
        def _exec(_url):
            res = requests.get(_url)
            print(res.text)

        if self.concurrent > 1:
            with futures.ThreadPoolExecutor(max_workers=self.concurrent) as executor:
                mappings = {executor.submit(_exec,
                                            self.url
                                            ): _ for _ in range(self.concurrent)}

            for future in futures.as_completed(mappings):
                future.result()
        else:
            _exec(self.url)



if __name__ == "__main__":
    _argv = sys.argv

    a_url = _argv[1]

    if len(_argv) > 2:
        a_concurrent = _argv[2]
        a_concurrent = int(a_concurrent)
    else:
        a_concurrent = 0

    sr = SimpleRequester(a_url, a_concurrent)
    sr.request()
