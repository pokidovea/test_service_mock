import json
from typing import Optional

from proxy.common.utils import bytes_, build_http_response, text_
from proxy.http.parser import HttpParser
from proxy.http.proxy import HttpProxyBasePlugin
from proxy.http.codes import httpStatusCodes


class ProposedRestApiPlugin(HttpProxyBasePlugin):
    """Mock responses for your upstream REST API.
    Used to test and develop client side applications
    without need of an actual upstream REST API server.
    Returns proposed REST API mock responses to the client
    without establishing upstream connection.
    Note: This plugin won't work if your client is making
    HTTPS connection to api.example.com.
    """

    API_SERVER = b'facebook.com'

    REST_API_SPEC = {
        b'/': {'message': 'Hello from Facebook'},
        b'/hi/': {'message': 'I already said you hello.'},
    }

    def before_upstream_connection(self, request: HttpParser) -> Optional[HttpParser]:
        # Return None to disable establishing connection to upstream
        # Most likely our api.example.com won't even exist under development
        # scenario
        return None

    def handle_client_request(self, request: HttpParser) -> Optional[HttpParser]:
        if request.host != self.API_SERVER:
            return request
        assert request.path
        if request.path in self.REST_API_SPEC:
            self.client.queue(memoryview(build_http_response(
                httpStatusCodes.OK,
                reason=b'OK',
                headers={b'Content-Type': b'application/json'},
                body=bytes_(json.dumps(
                    self.REST_API_SPEC[request.path]))
            )))
        else:
            self.client.queue(memoryview(build_http_response(
                httpStatusCodes.NOT_FOUND,
                reason=b'NOT FOUND', body=b'Not Found'
            )))
        return None

    def handle_upstream_chunk(self, chunk: memoryview) -> memoryview:
        return chunk

    def on_upstream_connection_close(self) -> None:
        pass
