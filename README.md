# OR-Tools with Hydra and MLFlow

- see also
    - https://github.com/cocomoff/ortools_with_hydra
- summary (recap.)
    - Original CVRP source
        - https://developers.google.com/optimization/routing/penalties
    - The source is modified as
        - function *main* receives the panlty value (default: 1000)
        - function *create_data_model* receives vehicle num. (default: 4. The upper bound is 4.)
- purpose
    - manage OR experiments using hydra and visualize them in mlflow