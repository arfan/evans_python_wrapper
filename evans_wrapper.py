import json
import os
import subprocess
import uuid

import util


class EvansWrapper:
    def __init__(self):
        self.enrich = None

    @staticmethod
    def __metadata_to_header(metadata):
        result_arr = []
        for key, value in metadata.items():
            result_arr.extend(["--header", f'{key}="{value}"'])

        return result_arr

    def call(self, proto_file, endpoint, host_port, payload=None, metadata=None, tls=True):
        if payload is None:
            payload = {}
        if metadata is None:
            metadata = {}

        self.enrich = None
        payload_str = json.dumps(payload)
        payload_file = f"payload_{str(uuid.uuid4())}.json"

        absolute_file_path = os.path.abspath(os.path.join(os.getcwd(), proto_file))
        absolute_folder_path = os.path.dirname(absolute_file_path)
        file_name = os.path.basename(absolute_file_path)

        absolute_payload_file_path = os.path.join(absolute_folder_path, payload_file)

        with open(absolute_payload_file_path, 'w') as file:
            file.write(payload_str)

        host, port = util.separate_host_and_port(host_port)

        command_array = ["evans",
                         "--tls" if tls else "",
                         "--path", absolute_folder_path,
                         "--proto", file_name,
                         "--file", absolute_payload_file_path,
                         "--host", host,
                         "-p", port,
                         "cli", "call", "--enrich", endpoint]

        metadata_header = self.__metadata_to_header(metadata)
        command_array.extend(metadata_header)

        all_command = f"cd {absolute_folder_path} && " + " ".join(command_array)

        process = subprocess.Popen(all_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        process_communicate = process.communicate()

        os.remove(absolute_payload_file_path)

        if len(process_communicate[1]):
            print(f"ERROR: [{process_communicate[1]}]")

        result, enrich = util.parse_result(process_communicate[0].decode())
        self.enrich = enrich

        return result, process_communicate[1]

    def get_enrich(self):
        return self.enrich
