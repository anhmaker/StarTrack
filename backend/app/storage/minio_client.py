import os
import io
import json
import requests
from minio import Minio
from minio.error import S3Error
from typing import Dict, Any, Optional

# MinIO client singleton
_minio_client: Optional[Minio] = None


def get_minio_client() -> Minio:
    """Get or create MinIO client singleton."""
    global _minio_client
    
    if _minio_client is None:
        endpoint = os.environ.get('MINIO_ENDPOINT', 'minio:9000')
        access_key = os.environ.get('MINIO_ACCESS_KEY', 'minioadmin')
        secret_key = os.environ.get('MINIO_SECRET_KEY', 'minioadmin')
        
        _minio_client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False
        )
    
    return _minio_client


def get_bucket_name() -> str:
    """Get bucket name from environment."""
    return os.environ.get('MINIO_BUCKET', 'apod-cache')


def ensure_bucket_exists() -> None:
    """Create bucket if it doesn't exist."""
    client = get_minio_client()
    bucket = get_bucket_name()
    
    try:
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)
            print(f"Created bucket: {bucket}")
    except S3Error as e:
        print(f"Error creating bucket: {e}")
        raise


def check_cached_data(date: str) -> bool:
    """Check if APOD data exists in cache for given date."""
    client = get_minio_client()
    bucket = get_bucket_name()
    
    try:
        client.stat_object(bucket, f"{date}/metadata.json")
        return True
    except S3Error:
        return False


def get_cached_json(date: str) -> Optional[Dict[str, Any]]:
    """Get cached JSON metadata for given date."""
    client = get_minio_client()
    bucket = get_bucket_name()
    
    try:
        response = client.get_object(bucket, f"{date}/metadata.json")
        data = json.loads(response.read().decode('utf-8'))
        response.close()
        response.release_conn()
        return data
    except S3Error:
        return None


def save_json(date: str, json_data: Dict[str, Any]) -> None:
    """Save JSON metadata to MinIO."""
    client = get_minio_client()
    bucket = get_bucket_name()
    
    ensure_bucket_exists()
    
    data_bytes = json.dumps(json_data).encode('utf-8')
    data_stream = io.BytesIO(data_bytes)
    
    client.put_object(
        bucket,
        f"{date}/metadata.json",
        data_stream,
        length=len(data_bytes),
        content_type='application/json'
    )


def download_and_save_image(date: str, image_url: str, hd: bool = False) -> str:
    """Download image from URL and save to MinIO."""
    client = get_minio_client()
    bucket = get_bucket_name()
    
    ensure_bucket_exists()
    
    # Download image
    response = requests.get(image_url, timeout=60)
    response.raise_for_status()
    
    # Determine content type
    content_type = response.headers.get('Content-Type', 'image/jpeg')
    
    # Determine filename
    filename = f"{date}/image_hd.jpg" if hd else f"{date}/image.jpg"
    
    # Upload to MinIO
    image_data = io.BytesIO(response.content)
    client.put_object(
        bucket,
        filename,
        image_data,
        length=len(response.content),
        content_type=content_type
    )
    
    return filename


def get_image_object(date: str, hd: bool = False):
    """Get image object from MinIO."""
    client = get_minio_client()
    bucket = get_bucket_name()
    
    filename = f"{date}/image_hd.jpg" if hd else f"{date}/image.jpg"
    
    try:
        return client.get_object(bucket, filename)
    except S3Error:
        return None


def get_presigned_url(date: str, hd: bool = False, expires: int = 3600) -> Optional[str]:
    """Generate presigned URL for image access."""
    client = get_minio_client()
    bucket = get_bucket_name()
    
    filename = f"{date}/image_hd.jpg" if hd else f"{date}/image.jpg"
    
    try:
        from datetime import timedelta
        url = client.presigned_get_object(
            bucket, 
            filename,
            expires=timedelta(seconds=expires)
        )
        return url
    except S3Error:
        return None

