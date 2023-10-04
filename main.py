from evans_wrapper import EvansWrapper

wrapper = EvansWrapper()
result, error = wrapper.call(
    proto_file="./sample_proto/hello.proto",
    endpoint="hello.HelloService.SayHello",
    host_port="localhost:9000",
    payload={
        "greeting": "Hello World",
    },
    metadata={},
    tls=False
)

print(result)
print(error)
print(wrapper.get_enrich())
