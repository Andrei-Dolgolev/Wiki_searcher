import requests
import httpx
from bs4 import BeautifulSoup
import asyncio

sem = asyncio.BoundedSemaphore(500)


class Racer:

    def __init__(self,start,end,stop_rule):

        # set initial
        self.start_url = start
        self.end_url = end

        self.answer = []

        self.stop_rule = True

        #start_state
        self.point_list = []
        self.graph = {}
        self.epohs = {0:0} # contain epochs and start index of epochs


    def search_from_start_to_end(self):
        """
        Function start epoch from first url and search via all directions
        1 processed all available and not visited urls its one epoch
        """

        epoch = 0
        points = [self.start_url]
        results = []
        [self.point_list.append(i) for i in points]

        while self.end_url not in results:

            print("Epoh", epoch)
            loop = asyncio.new_event_loop()

            # start loop via available new urls
            results = loop.run_until_complete(self.next_epoh(range(self.epohs[epoch],len(self.point_list))))

            for url, urls in results:

                # add knowledge about new node
                self.graph[url] = []

                urls = set(urls)

                for child_url in urls:
                    # if protocol no supplied
                    if not 'https://' in child_url:
                        child_url = ''.join(('https://en.wikipedia.org',child_url)) # another subdomains have full url

                    # add new url to list of all urls and to parent node
                    if child_url not in self.point_list:
                        self.point_list.append(child_url)
                        self.graph[url].append(len(self.point_list) - 1)
                    else:
                        self.graph[url].append(self.point_list.index(child_url))


            epoch += 1
            self.epohs[epoch] = len(points)
            loop.close()

        visited = set()  # Set to keep track of visited nodes.

        # Driver Code
        self.deep_search(visited, self.graph, self.start_url)
        print(self.answer)


    def deep_search(self, visited, graph, node):
        """

        :param visited:
        :param graph:
        :param node:
        :return: list of urls

        deep graph search

        """

        if node not in visited:
            print(node)
            visited.add(node)
            if graph[node]:
                for neighbour in graph[node]:
                    response = self.deep_search(visited, graph, neighbour)
                    if response:
                        self.answer.append(node)
                        return True
            else: #end node
                if node == self.end_url:
                    return node
                else:
                    return False


    async def next_epoh(self,ids_of_urls):

        """
        Processing new urls
        :param ids_of_urls:
        :return:
        """

        sem = asyncio.Semaphore(500)
        timeout = httpx.Timeout(10.0, connect=5)
        limits = httpx.Limits(max_keepalive=1000, max_connections=100)

        print(len(ids_of_urls))

        async with httpx.AsyncClient(limits=limits, timeout=timeout) as session:
            response_list = await asyncio.gather(*[self.bound_fetch(sem,session,id_of_url) for id_of_url in ids_of_urls])

        response_list = [i for i in response_list if i] # clear exceptions
        return response_list

    async def bound_fetch(self, sem, session, id_of_url):
        """
        limit our workers
        :param sem:
        :param session:
        :param id_of_url:
        :return:
        """
        async with sem:
            return await self.fetch(session, id_of_url)

    async def fetch(self,session,id_of_url):

        """
        Go to article page and upload all links except functional and red links type
        :param session:
        :param id_of_url:
        :return:
        """

        url = self.point_list[id_of_url]
        print(url)
        try:
            res = await session.get(url)
        except:
            return None
        soup = BeautifulSoup(res.text,'html.parser')
        #print(res.text)
        article = soup.select_one('#content')
        urls = [a.get('href') for a in article.find_all('a', href=True)
                                                                        if '/wiki/' in a['href']
                                                                        and not 'redlink' in a['href']
                                                                        and not 'Featured_articles' in a['href']
                                                                        and not '[' in a['href']
                                                                        and not '(' in a['href']
                                                                        and not '.jpg' in a['href']
                                                                        and not 'Special:' in a['href']
                                                                        and not 'Category:' in a['href']
                                                                        and not 'File:' in a['href']
                                                                        and not 'Help:' in a['href']
                                                                        and not 'Template:' in a['href']
                                                                        ]

        #print(url)
        return url,urls


    def search_one_to_many(self):
        """
        List realization
        :return:
        """
        pass

    def search_route_via_similar_signature(self):
        """
        Need add read country and anothre fields
        :return:
        """
        pass

    def languege_level(self):
        """
        Search in another launges zone
        :return:
        """
        pass



z = Racer('https://en.wikipedia.org/wiki/Battle_of_Cr%C3%A9cy','https://en.wikipedia.org/wiki/Wehrmacht',False)

z.search_from_start_to_end()