from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import random
import time

# Configuration
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "my-token"
INFLUXDB_ORG = "my-org"
INFLUXDB_BUCKET = "cpu_usage"


def setup_influxdb():
    """Sets up InfluxDB bucket and verifies connection."""
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        health = client.ping()
        if health:
            raise Exception("InfluxDB is not healthy. Check your setup!")
        print("InfluxDB connected successfully.")

        # Create a bucket if it doesn't exist
        buckets_api = client.buckets_api()
        buckets = buckets_api.find_bucket_by_name(INFLUXDB_BUCKET)
        if not buckets:
            buckets_api.create_bucket(bucket_name=INFLUXDB_BUCKET, org=INFLUXDB_ORG)
            print(f"Bucket '{INFLUXDB_BUCKET}' created.")
        else:
            print(f"Bucket '{INFLUXDB_BUCKET}' already exists.")


def write_cpu_data():
    """Writes random CPU usage data to InfluxDB."""
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)

        for _ in range(10):  # Simulate 10 data points
            cpu_usage = random.uniform(10, 100)
            point = (
                Point("cpu")
                .tag("host", "server01")
                .field("usage", cpu_usage)
                .time(datetime.now())
            )
            write_api.write(bucket=INFLUXDB_BUCKET, record=point)
            print(f"Written: {point.to_line_protocol()}")
            time.sleep(1)  # Simulate data arrival over time


def query_cpu_data():
    """Queries CPU usage data from InfluxDB."""
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
          |> range(start: -1h)
          |> filter(fn: (r) => r._measurement == "cpu" and r._field == "usage")
          |> mean()
        '''
        query_api = client.query_api()
        tables = query_api.query(query)
        for table in tables:
            for record in table.records:
                print(f"Average CPU Usage: {record['_value']:.2f}%")


if __name__ == "__main__":
    print("Setting up InfluxDB...")
    setup_influxdb()

    print("\nWriting CPU usage data...")
    write_cpu_data()

    print("\nQuerying CPU usage data...")
    query_cpu_data()
