"""
Example DAG for demonstrating behavior of Datasets feature.
Notes on usage:
Turn on all the dags.
DAG dataset_produces_1 should run because it's on a schedule.
After dataset_produces_1 runs, dataset_consumes_1 should be triggered immediately
because its only dataset dependency is managed by dataset_produces_1.
No other dags should be triggered.  Note that even though dataset_consumes_1_and_2 depends on
the dataset in dataset_produces_1, it will not be triggered until dataset_produces_2 runs
(and dataset_produces_2 is left with no schedule so that we can trigger it manually).
Next, trigger dataset_produces_2.  After dataset_produces_2 finishes,
dataset_consumes_1_and_2 should run.
Dags dataset_consumes_1_never_scheduled and dataset_consumes_unknown_never_scheduled should not run because
they depend on datasets that never get updated.
"""
from __future__ import annotations
import pendulum
from airflow import DAG, Dataset
from airflow.operators.bash import BashOperator
dag1_dataset = Dataset('s3://dag1/output_1.txt', extra={'hi': 'bye'})
dag2_dataset = Dataset('s3://dag2/output_1.txt', extra={'hi': 'bye'})

with DAG(dag_id='data_retrieve',catchup=False,start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
         schedule='@daily',tags=['produces', 'dataset-scheduled']) as dag1:
  BashOperator(outlets=[dag1_dataset], task_id='producing_task_1', bash_command="sleep 5")

with DAG(dag_id='dataset_produces_2',catchup=False,start_date=pendulum.datetime(2021, 1, 1, tz="UTC")
         ,schedule=None,tags=['produces', 'dataset-scheduled']) as dag2:
  BashOperator(outlets=[dag2_dataset], task_id='producing_task_2', bash_command="sleep 5")

# [START dag_dep]
with DAG(
    dag_id='dataset_consumes_1',
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=[dag1_dataset],
    tags=['consumes', 'dataset-scheduled'],
) as dag3:
    # [END dag_dep]
    BashOperator(
        outlets=[Dataset('s3://consuming_1_task/dataset_other.txt')],
        task_id='consuming_1',
        bash_command="sleep 5",
    )

with DAG(
    dag_id='dataset_consumes_1_and_2',
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=[dag1_dataset, dag2_dataset],
    tags=['consumes', 'dataset-scheduled'],
) as dag4:
    BashOperator(
        outlets=[Dataset('s3://consuming_2_task/dataset_other_unknown.txt')],
        task_id='consuming_2',
        bash_command="sleep 5",
    )

with DAG(
    dag_id='dataset_consumes_1_never_scheduled',
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=[
        dag1_dataset,
        Dataset('s3://this-dataset-doesnt-get-triggered'),
    ],
    tags=['consumes', 'dataset-scheduled'],
) as dag5:
    BashOperator(
        outlets=[Dataset('s3://consuming_2_task/dataset_other_unknown.txt')],
        task_id='consuming_3',
        bash_command="sleep 5",
    )

with DAG(
    dag_id='dataset_consumes_unknown_never_scheduled',
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=[
        Dataset('s3://unrelated/dataset3.txt'),
        Dataset('s3://unrelated/dataset_other_unknown.txt'),
    ],
    tags=['dataset-scheduled'],
) as dag6:
    BashOperator(
        task_id='unrelated_task',
        outlets=[Dataset('s3://unrelated_task/dataset_other_unknown.txt')],
        bash_command="sleep 5",
    )
