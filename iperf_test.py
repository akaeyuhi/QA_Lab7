import pytest
from conftest import client
from iperf import parser

class TestSuite:
    @pytest.mark.parametrize("expected_min_transfer,expected_min_bandwidth", [
        (100, 0.02), 
        (100, 0.5), 
        (100, 1), 
        (200, 3),
        (500, 0.2),
        (200, 0.4),
    ])
    def test_iperf3_client_connection(self, client, expected_min_transfer, expected_min_bandwidth):
        stdout, stderr = client

        assert stdout.strip(), "Вивід iperf-клієнта порожній"

        assert not stderr.strip(), f"Помилка iperf-клієнта: {stderr}"

        parsed_intervals = parser(stdout)

        for interval in parsed_intervals:
            assert interval['Bitrate'] > expected_min_bandwidth, \
                f"Пропускна здатність менше, ніж очікувана мінімальна величина {expected_min_bandwidth} Gbps"
            assert interval['Transfer'] > expected_min_transfer, \
                f"Transfer менше, ніж очікувана мінімальна величина {expected_min_transfer} Mbytes"