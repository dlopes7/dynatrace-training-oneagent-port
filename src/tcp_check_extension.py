import socket

from ruxit.api.base_plugin import BasePlugin
from ruxit.api.selectors import HostSelector


class TCPCheckExtension(BasePlugin):

    def query(self, **kwargs):

        raw_targets: str = self.config.get("targets")
        for line in raw_targets.splitlines():
            self.logger.info(f"Processing line: {line}")
            host, port = line.split(":")
            result = test_port(host, int(port))
            self.logger.info(f"Result for {line}: {result}")

            result = "OK" if result else "ERROR"
            self.results_builder.state_metric("tcp_state", result, entity_selector=HostSelector(), dimensions={"Target": line})


def test_port(ip: str, port: int) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((ip, port))
    sock.close()

    return result == 0


