from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone
import random
import time

# Configuration
INFLUXDB_URL = "http://localhost:8086"
# I am aware that I am pushing this token into github but it's only a sample project
# I decided not to remove it, but normally I would use this information:
# https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
INFLUXDB_TOKEN = "13BvEwt0glL-7PXcH_3i40BGacC8hRp4MqPjieqrW3uIhuYlCNhfw_TrfshtEXsJEozBZi6keoRhPuc1OzArFg=="
INFLUXDB_ORG = "Sample Project"
INFLUXDB_BUCKET = "cpu_usage"


def setup_influxdb():
    """Sets up InfluxDB bucket and verifies connection."""
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        health = client.ping()
        if not health:  # Corrected condition
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

        for _ in range(10):  # Corrected loop syntax
            cpu_usage = random.uniform(10, 100)  # Fixed variable name
            point = (
                Point("cpu")
                .tag("host", "server01")
                .field("usage", cpu_usage)
                .time(datetime.now(timezone.utc))  # Use UTC time
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


if __name__ == "__main__":  # Corrected name spelling
    print("Setting up InfluxDB...")
    setup_influxdb()

    print("\nWriting CPU usage data...")
    write_cpu_data()

    print("\nQuerying CPU usage data...")
    query_cpu_data()
