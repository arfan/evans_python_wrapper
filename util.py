def separate_host_and_port(input_string):
    parts = input_string.split(':')

    host = parts[0]
    port = parts[1]

    return host, port


def parse_result(result):
    enrich = dict()
    start_json = False
    json_result = ""
    for line in result.splitlines():
        if line == "{":
            start_json = True

        if start_json:
            json_result = json_result + line

        if line == "}":
            start_json = False

        if ":" in line and not line.strip().startswith('"'):
            line_split = line.split(":")
            enrich[line_split[0].strip()] = line_split[1].strip().strip('"')

    return json_result, enrich
