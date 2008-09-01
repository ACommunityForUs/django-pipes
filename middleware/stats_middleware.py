from django.conf import settings

import pipes

class PipesStatsMiddleware:
    def process_response(self, request, response):
        if settings.DEBUG:
            
            queries = pipes.debug_stats.queries
            cached_queries = filter(lambda query: query['found_in_cache'], queries)
            failed_queries = filter(lambda query: query['failed'], queries)
            
            print "\n================== Pipes Usage Summary ==========================="
            print "Total: %d   Found in cache: %d   Fetched from remote: %d   Failed: %d\n" % (
                    len(queries), len(cached_queries),
                    len(queries) - len(cached_queries), len(failed_queries)
                )
            for idx, query in enumerate(queries):
                if query['failed']:
                    status = "FAILED"
                elif query['found_in_cache']:
                    status = "FETCHED FROM CACHE"
                else:
                    status = "FETCHED FROM REMOTE"
                print "%d: %s : %s" % (idx, status, query['url'])
            print "====================================================================\n"
        return response
