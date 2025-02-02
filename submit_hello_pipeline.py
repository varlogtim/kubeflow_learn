from tools.kfp_auth import get_kfp_client_from_env


client = get_kfp_client_from_env()

run = client.create_run_from_pipeline_package(
    'pipeline.yaml',
    arguments={
        'recipient': 'World',
    },
)
