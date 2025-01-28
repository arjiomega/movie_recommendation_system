from airflow.operators.bash import BashOperator

class WarehouseTasks:

    def build_data_warehouse(self) -> str:
        vars_dict = {
            "start_date": "{{ ds }}",
            "end_date": "{{ next_ds }}"
        }
        vars_str = str(vars_dict).replace("'", "\"") 
        return BashOperator(
            task_id=f"build_data_warehouse",
            bash_command=f"dbt run --vars '{vars_str}'",
            cwd='/opt/airflow'
        )