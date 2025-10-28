import boto3, csv, io, os
from datetime import datetime

s3 = boto3.client('s3')

BUCKET = os.environ.get('BUCKET')
INPUT_PREFIX = os.environ.get('INPUT_PREFIX', 'incoming/')
OUTPUT_PREFIX = os.environ.get('OUTPUT_PREFIX', 'processed/')

def process_csv_text(csv_text):
    input_io = io.StringIO(csv_text)
    reader = csv.DictReader(input_io)
    fieldnames = list(reader.fieldnames or [])
    if 'processed_at' not in fieldnames:
        fieldnames.append('processed_at')

    output_io = io.StringIO()
    writer = csv.DictWriter(output_io, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        temp_val = (row.get('temp') or row.get('temperature') or row.get('Temperature') or '').strip()
        if temp_val == '':
            continue
        row['processed_at'] = datetime.utcnow().isoformat()
        writer.writerow(row)

    return output_io.getvalue()

def lambda_handler(event, context):
    for record in event.get('Records', []):
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        if not key.startswith(INPUT_PREFIX):
            print(f"Skipping (not in prefix): {key}")
            continue
        try:
            resp = s3.get_object(Bucket=bucket, Key=key)
            raw = resp['Body'].read().decode('utf-8')
        except Exception as e:
            print(f"Error reading s3://{bucket}/{key}: {e}")
            continue

        cleaned = process_csv_text(raw)
        filename = key.split('/')[-1]
        out_key = f"{OUTPUT_PREFIX.rstrip('/')}/{filename}"
        try:
            s3.put_object(Bucket=bucket, Key=out_key, Body=cleaned.encode('utf-8'))
            print(f"Wrote cleaned file to s3://{bucket}/{out_key}")
        except Exception as e:
            print(f"Error writing s3://{bucket}/{out_key}: {e}")

    return {"status": "ok"}
