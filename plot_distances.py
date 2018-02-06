import argparse
import datetime
import logging
import time

import arc852.cli_args as cli
import plotly.graph_objs as go
import plotly.plotly as py
import plotly.tools as tls
from arc852.constants import LOG_LEVEL
from arc852.grpc_support import TimeoutException
from arc852.utils import setup_logging

from http_distance_client import HttpDistanceClient

logger = logging.getLogger(__name__)


def main():
    # Parse CLI args
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", dest="url", default="localhost:8080", help="Distance server URL")
    cli.log_level(parser)
    args = vars(parser.parse_args())

    # Setup logging
    setup_logging(level=args[LOG_LEVEL])

    stream_ids = tls.get_credentials_file()['stream_ids']
    stream_id = stream_ids[1]

    # Declare graph
    graph = go.Scatter(x=[], y=[], mode='lines+markers', stream=dict(token=stream_id, maxpoints=80))
    data = go.Data([graph])
    layout = go.Layout(title='Distances', yaxis=go.YAxis(range=[100]))
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='plot-positions')

    # Write data
    stream = py.Stream(stream_id)
    stream.open()

    logger.info("Opening plot.ly tab")
    time.sleep(5)

    prev_pos = None

    try:
        with HttpDistanceClient(args["url"]) as distances:
            while True:
                try:
                    val = distances.value()

                    if val.distance == -1:
                        prev_pos = None
                        continue

                    y = val.distance
                    prev_pos = y

                # No change in value
                except TimeoutException:
                    y = prev_pos

                x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

                stream.write(dict(x=x, y=y))
                time.sleep(.10)

    except KeyboardInterrupt:
        pass
    finally:
        stream.close()

    logger.info("Exiting...")


if __name__ == "__main__":
    main()
