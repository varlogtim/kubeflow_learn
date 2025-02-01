from kfp import dsl, compiler


@dsl.component(base_image="python:3.12")
def say_hello(name: str) -> str:
    hello_text = f'Hello, {name}!'
    print(hello_text)
    return hello_text

@dsl.pipeline
def hello_pipeline(recipient: str) -> str:
    hello_task = say_hello(name=recipient)
    return hello_task.output


compiler.Compiler().compile(
    hello_pipeline,
    'pipeline.yaml',
)
