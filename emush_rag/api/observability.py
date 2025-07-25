from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)

resource = Resource.create(attributes={SERVICE_NAME: "emush-rag"})

tracer_provider = TracerProvider(resource=resource)
jaeger_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True))
tracer_provider.add_span_processor(jaeger_processor)

trace.set_tracer_provider(tracer_provider)
tracer = trace.get_tracer("my.tracer", tracer_provider=tracer_provider)
