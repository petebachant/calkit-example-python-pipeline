"""A Python script that creates a DVC pipeline.

Include scheduling?
We could define a once per day task,
and we break the DVC pipeline up accordingly.
Will want a way to distribute the stages.

If someone runs

    calkit run

from the terminal,
and calkit sees a calkit.py or pipeline.py file?
we convert the script into a DVC pipeline then run that

This would actually be a pure extension of the existing system

Kind of similar to Dagster

Should this handle chunked dependencies,
automatically breaking the logic into multiple stages,
one per chunk or partition.

I guess it would also need to partition the outputs.

Is it possible this would be scalable?
We'd want DVC to remotely run necessary stages,
either in processes or different machines,
in parallel.

Stage command could look like this to enable distributed workers,
who run their stage and push

    calkit run-stage-remote --remote-name my-hpc --stage get_data_partition_1 some command

    calkit run-stage-remote --worker-pool some command

calkit run detects any remote runs and waits until they're all done,
then collects up all of the commits they merged together?
Git history then becomes a log of tasks being run?

We could query for task history from git log?

Can we also store different partitions on different machines,
or have them write direct to the DVC remote,
so our local project can stay clean.

Can we make this work with marimo notebooks?

Can we schedule these pipeline runs in the cloud?
GitHub Actions is an option.
That could enable event-driven workflows, e.g., run the pipeline
and push on all pushes to main.

"""

from typing import Annotated

import plotly.graph_objects as go
from calkit.decorators import stage
from calkit.pipeline import Dataset, Dependency, Figure, Output, stage


@stage
def collect_data() -> Annotated[
    pd.DataFrame,
    Dataset(path="data/something.parquet", title="The data"),
]:
    return pd.DataFrame(range(5))


@stage
def plot_data(
    data: Annotated[pd.DataFrame, Dataset(path="data/something.parquet")]
) -> Annotated[
    go.Figure, Figure(path="figures/plot.json", title="The figure")
]:
    return data.plot(backend="plotly")
