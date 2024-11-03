[Protocol Buffers](https://protobuf.dev/) are a language-neutral, platform-neutral extensible mechanism for serializing
structured data.
It’s like JSON, except it’s smaller and faster, and it generates native language bindings. You define how you want your
data to be structured once, then you can use special generated source code to easily write and read your structured data
to and from a variety of data streams and using a variety of languages.

Protocol buffers are a combination of the definition language (created in `.proto` files), the code that the proto
compiler generates to interface with data, language-specific runtime libraries, the serialization format for data that
is written to a file (or sent across a network connection), and the serialized data.

Some of the advantages of using protocol buffers include:

- Compact data storage
- Fast parsing
- Availability in many programming languages
- Optimized functionality through automatically-generated classes

**Because of its strict definition of the interface of the data, it is a good choice for making sure that the created logs
adhere to [Foxglove's schemas](https://github.com/foxglove/schemas/tree/main/schemas/proto/foxglove).**
