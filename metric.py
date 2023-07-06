import subprocess
import json
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import generate_latest
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource
import time
from nvitop import Device, GpuProcess, colored
import os
import docker

class GpuSmCollector(object):
    def __init__(self, sm_target_port=9009, polling_interval_seconds=5):
        self.sm_target_port = sm_target_port
        self.polling_interval_seconds = polling_interval_seconds

    def run_metrics_loop(self):
        """Metrics fetching loop"""
        while True:
            self.collect()
            time.sleep(self.polling_interval_seconds)

    def collect(self):
        sm = GaugeMetricFamily('gpu_process', 'GPU SM Utilization', labels=['gpu', 'pid', 'name'])
        client = docker.from_env()
        containers = client.containers.list()
        devices = Device.all()
        device_list = []
        for i, dev in enumerate(devices):
            gpu_label = f"GPU{i+1}"
            device_dict = {gpu_label: dev.bus_id()}
            device_list.append(device_dict)
        for device in devices:
            processes = device.processes()
            if len(processes) > 0:
                processes = GpuProcess.take_snapshots(processes.values(), failsafe=True)
                for snapshot in processes:
                    gpu_label = next((key for device_dict in device_list for key, value in device_dict.items() if value == device.bus_id()), None)
                    pid = str(snapshot.pid)

                    container_name = None
                    for container in containers:
                        if container.status == 'running' and container.attrs['State']['Pid'] == snapshot.pid:
                            container_name = container.name
                            break
                    sm.add_metric([gpu_label, pid, container_name], float(snapshot.gpu_sm_utilization))
            else:
                print(colored('  - No Running Processes', attrs=('bold',)))
        return [sm]


class MetricsResource(Resource):
    isLeaf = True

    def __init__(self, collector):
        self.collector = collector
        Resource.__init__(self)

    def render_GET(self, request):
        output = generate_latest(REGISTRY)
        request.setHeader("Content-Type", "text/plain; version=0.0.4")
        request.setHeader("Content-Length", str(len(output)))
        return output


def main():
    """Main entry point"""
    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "5"))
    exporter_port = int(os.getenv("EXPORTER_PORT", "9009"))

    sm_metrics = GpuSmCollector(
        sm_target_port=exporter_port,
        polling_interval_seconds=polling_interval_seconds
    )
    REGISTRY.register(sm_metrics)

    metrics_resource = MetricsResource(sm_metrics)
    factory = Site(metrics_resource)
    reactor.listenTCP(exporter_port, factory)
    reactor.run()


if __name__ == "__main__":
    main()