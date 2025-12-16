"""
MinIO Proxy - provides endpoints for accessing cached images
"""
from flask import Blueprint, Response, jsonify, send_file
from app.storage.minio_client import get_image_object, get_presigned_url
import io

storage_bp = Blueprint('storage', __name__)


@storage_bp.route('/storage/image/<date>')
def get_image(date: str):
    """Get regular image for given date."""
    try:
        # Try to get image from MinIO
        image_obj = get_image_object(date, hd=False)
        
        if image_obj is None:
            return jsonify({'error': 'Image not found'}), 404
        
        # Read image data
        image_data = image_obj.read()
        image_obj.close()
        image_obj.release_conn()
        
        # Return image
        return Response(
            image_data,
            mimetype='image/jpeg',
            headers={
                'Cache-Control': 'public, max-age=86400',  # Cache for 1 day
                'Content-Type': 'image/jpeg'
            }
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@storage_bp.route('/storage/image/<date>/hd')
def get_hd_image(date: str):
    """Get HD image for given date."""
    try:
        # Try to get HD image from MinIO
        image_obj = get_image_object(date, hd=True)
        
        if image_obj is None:
            return jsonify({'error': 'HD image not found'}), 404
        
        # Read image data
        image_data = image_obj.read()
        image_obj.close()
        image_obj.release_conn()
        
        # Return image
        return Response(
            image_data,
            mimetype='image/jpeg',
            headers={
                'Cache-Control': 'public, max-age=86400',  # Cache for 1 day
                'Content-Type': 'image/jpeg',
                'Content-Disposition': f'attachment; filename="NASA_APOD_{date}_HD.jpg"'
            }
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@storage_bp.route('/storage/image/<date>/url')
def get_image_url(date: str):
    """Get presigned URL for regular image."""
    try:
        url = get_presigned_url(date, hd=False, expires=3600)
        
        if url is None:
            return jsonify({'error': 'Image not found'}), 404
        
        return jsonify({'url': url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@storage_bp.route('/storage/image/<date>/hd/url')
def get_hd_image_url(date: str):
    """Get presigned URL for HD image."""
    try:
        url = get_presigned_url(date, hd=True, expires=3600)
        
        if url is None:
            return jsonify({'error': 'HD image not found'}), 404
        
        return jsonify({'url': url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
