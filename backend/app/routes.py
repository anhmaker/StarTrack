from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta

api_bp = Blueprint('api', __name__)


def validate_date(date_str: str) -> tuple[bool, str]:
    """Validate date string and check if it's within allowed range."""
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD"
    
    today = datetime.now().date()
    min_date = today - timedelta(days=30)
    
    if date > today:
        return False, "Date cannot be in the future"
    if date < min_date:
        return False, f"Date must be within last 30 days (after {min_date})"
    
    return True, ""


@api_bp.route('/api/apod')
def get_apod():
    """Get Astronomy Picture of the Day."""
    date_str = request.args.get('date')
    
    if date_str:
        is_valid, error_msg = validate_date(date_str)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
    else:
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    # Import here to avoid circular imports
    from app.apod_service import get_apod_data
    
    try:
        data = get_apod_data(date_str)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/api/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})

