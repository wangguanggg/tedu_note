from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
import re
class VisitLimited(MiddlewareMixin):
    visit_times = {}
    def process_request(self, request):
        print("My process_reqeust do")
        ip_address = request.META['REMOTE_ADDR']
        path_url = request.path_info
        if not re.match("^/test", path_url):
            return
        times = self.visit_times.get(ip_address, 0)
        print(ip_address, "已经访问", times)
        self.visit_times[ip_address] = times + 1
        if times < 5:
            return
        else:
            return HttpResponse("您访问次数过多")

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print("My process_view do")

    def process_response(self, request, response):
        print("My process_response do")
        return response
