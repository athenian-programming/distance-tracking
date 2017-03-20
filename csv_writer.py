import argparse

from simple_distance_client import DistanceClient

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", dest="url", required=True, help="Distance server URL")
    parser.add_argument("-f", "--file", dest="file", required=True, help="CSV filename")
    args = vars(parser.parse_args())

    distances = DistanceClient(args["url"])

    with open(args["file"], 'w') as file:
        for val in distances.get_values():
            print("Wrote: {0}, {1}".format(val.elapsed, val.distance))
            file.write("{0}, {1}\n".format(val.elapsed, val.distance))

    print("Exited...")
